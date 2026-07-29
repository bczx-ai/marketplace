# -*- coding: utf-8 -*-
"""
浏览器自动化爬虫模块 v1.0 (browser_scraper.py)

当常规 HTTP 爬虫被反爬拦截时，自动启动真实浏览器模拟人工操作：
  - 可见窗口模式（非 headless），模拟真人浏览
  - 隐身上下文（Stealth），绕过反爬检测
  - Cookie / 弹窗自动处理
  - 等待特定元素出现后提取数据
  - 自动滚动加载懒加载内容
  - 截图保存用于人工验证
  - 登录流程支持（可选）
  - 与 http_utils 降级链无缝衔接

依赖：pip install playwright && playwright install chromium
缺失时所有方法返回 None 并提示安装命令，不影响其他模块。

用法：
  from browser_scraper import BrowserScraper
  bs = BrowserScraper(headless=False)  # 可见模式，便于观察
  html = bs.fetch("https://www.example.com")
  # 或提取特定数据
  data = bs.extract_text("https://www.example.com", selector=".content")
  # 截图留存
  bs.screenshot("https://www.example.com", "output/shot.png")
"""
from __future__ import annotations

import json
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable

try:
    from playwright.sync_api import sync_playwright, Browser, Page, BrowserContext
    from playwright.sync_api import TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Browser = None  # type: ignore
    Page = None     # type: ignore

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR / "data"
BROWSER_CACHE_DIR = DATA_DIR / "browser_cache"
BROWSER_CACHE_DIR.mkdir(exist_ok=True, parents=True)
SCREENSHOT_DIR = DATA_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True, parents=True)

INSTALL_HINT = (
    "浏览器自动化模块需要 Playwright。请安装：\n"
    "  pip install playwright\n"
    "  playwright install chromium\n"
    "Mac/Linux 用户可能还需要: playwright install-deps chromium"
)

# ── 反检测隐身脚本 ─────────────────────────────────────────────
STEALTH_JS = """
// 隐藏 webdriver 标记
Object.defineProperty(navigator, 'webdriver', { get: () => false });
// 伪造 plugins 数组
Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
// 伪造 languages
Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN','zh','en'] });
// 移除 PhantomJS 痕迹
delete window.callPhantom;
"""

# ── 常见 Cookie 弹窗选择器 ─────────────────────────────────────
COOKIE_CONSENT_SELECTORS = [
    # 中文
    "button:has-text('同意')", "button:has-text('接受')", "button:has-text('确定')",
    "button:has-text('知道了')", "button:has-text('允许')",
    "a:has-text('同意')", "span:has-text('同意')",
    ".cookie-accept", ".cookie-consent button",
    # 英文
    "button:has-text('Accept')", "button:has-text('Accept All')",
    "button:has-text('Agree')", "button:has-text('OK')",
    "button:has-text('Got it')", "button:has-text('I agree')",
    "button:has-text('Allow All')", "button:has-text('Consent')",
    # 通用
    "[aria-label='Accept cookies']", "[data-testid='cookie-accept']",
    "#accept-cookies", ".accept-cookies", "[id*='cookie'] button",
    ".cc-btn", ".cc_btn", ".cookie-btn",
]


class BrowserScraper:
    """浏览器自动化爬虫 — 类人操作模式

    headless=False: 可见窗口，随机延迟，模拟真人体浏览行为
    headless=True:  后台运行，速度更快但部分网站会检测到
    stealth=True:   注入反检测脚本，隐藏 webdriver 标记
    """

    def __init__(self, headless: bool = False, stealth: bool = True,
                 timeout_ms: int = 30000, viewport: dict = None):
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(INSTALL_HINT)
        self.headless = headless
        self.stealth = stealth
        self.timeout_ms = timeout_ms
        self.viewport = viewport or {"width": 1920, "height": 1080}
        self._playwright = None
        self._browser = None
        self._context = None
        self._last_page = None

    # ── 生命周期 ─────────────────────────────────────────────

    def start(self):
        """启动浏览器（单例复用）。"""
        if self._browser is not None:
            return
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=self.headless,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )
        self._context = self._browser.new_context(
            viewport=self.viewport,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            ),
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        if self.stealth:
            self._context.add_init_script(STEALTH_JS)

    def stop(self):
        """关闭浏览器释放资源。"""
        if self._context:
            self._context.close()
            self._context = None
        if self._browser:
            self._browser.close()
            self._browser = None
        if self._playwright:
            try:
                self._playwright.stop()
            except Exception:
                pass
            self._playwright = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def new_page(self) -> Page:
        """创建新页面（带隐身脚本）。"""
        self.start()
        page = self._context.new_page()
        page.set_default_timeout(self.timeout_ms)
        self._last_page = page
        return page

    # ── 核心抓取 ─────────────────────────────────────────────

    def fetch(self, url: str, wait_until: str = "domcontentloaded",
              wait_selector: str = None, scroll: bool = False,
              dismiss_cookies: bool = True) -> Optional[str]:
        """打开网页并返回完整 HTML。

        wait_until: domcontentloaded / load / networkidle
        wait_selector: 等待该 CSS 选择器出现后再提取
        scroll: 是否滚动页面加载懒加载内容
        dismiss_cookies: 是否自动点击 Cookie 弹窗
        """
        if not PLAYWRIGHT_AVAILABLE:
            print(INSTALL_HINT, file=sys.stderr)
            return None
        try:
            page = self.new_page()
            page.goto(url, wait_until=wait_until, timeout=self.timeout_ms)
            self._human_delay(0.5, 1.5)

            if dismiss_cookies:
                self._dismiss_cookie_popup(page)

            if wait_selector:
                page.wait_for_selector(wait_selector, timeout=self.timeout_ms)
                self._human_delay(0.3, 0.8)

            if scroll:
                self._auto_scroll(page)

            html = page.content()
            page.close()
            return html
        except PlaywrightTimeout:
            return None
        except Exception as e:
            print(f"[BrowserScraper] fetch 失败: {e}", file=sys.stderr)
            return None

    def extract_text(self, url: str, selector: str = "body",
                     wait_selector: str = None, scroll: bool = False,
                     dismiss_cookies: bool = True) -> Optional[str]:
        """提取指定元素的文本内容。"""
        try:
            page = self.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            self._human_delay(0.5, 1.5)

            if dismiss_cookies:
                self._dismiss_cookie_popup(page)

            if wait_selector:
                page.wait_for_selector(wait_selector, timeout=self.timeout_ms)

            if scroll:
                self._auto_scroll(page)

            text = page.text_content(selector, timeout=self.timeout_ms)
            page.close()
            return text.strip() if text else None
        except PlaywrightTimeout:
            return None
        except Exception as e:
            print(f"[BrowserScraper] extract_text 失败: {e}", file=sys.stderr)
            return None

    def extract_multiple(self, url: str, selectors: Dict[str, str],
                         **kwargs) -> Dict[str, Optional[str]]:
        """批量提取多个选择器的文本。selectors: {key: css_selector}"""
        results = {}
        try:
            page = self.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            self._human_delay(0.5, 1.5)
            if kwargs.get("dismiss_cookies", True):
                self._dismiss_cookie_popup(page)
            if kwargs.get("scroll", False):
                self._auto_scroll(page)

            for key, sel in selectors.items():
                try:
                    el = page.query_selector(sel)
                    results[key] = el.text_content().strip() if el else None
                except Exception:
                    results[key] = None
            page.close()
        except Exception as e:
            print(f"[BrowserScraper] extract_multiple 失败: {e}", file=sys.stderr)
        return results

    def extract_table(self, url: str, table_selector: str = "table",
                      **kwargs) -> List[Dict[str, str]]:
        """提取 HTML 表格为 dict 列表。"""
        rows_data = []
        try:
            page = self.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            self._human_delay(0.5, 1.5)
            if kwargs.get("dismiss_cookies", True):
                self._dismiss_cookie_popup(page)
            if kwargs.get("scroll", False):
                self._auto_scroll(page)

            rows = page.query_selector_all(f"{table_selector} tr")
            if not rows:
                return rows_data

            # 第一行作表头
            headers = [th.text_content().strip()
                       for th in rows[0].query_selector_all("th,td")]

            for row in rows[1:]:
                cells = [td.text_content().strip()
                         for td in row.query_selector_all("td")]
                if cells:
                    row_dict = {}
                    for i, cell in enumerate(cells):
                        key = headers[i] if i < len(headers) else f"col_{i}"
                        row_dict[key] = cell
                    rows_data.append(row_dict)
            page.close()
        except Exception as e:
            print(f"[BrowserScraper] extract_table 失败: {e}", file=sys.stderr)
        return rows_data

    # ── 截图 ─────────────────────────────────────────────────

    def screenshot(self, url: str, output_path: str = None,
                   full_page: bool = True, **kwargs) -> Optional[str]:
        """打开网页并截图保存。返回保存路径。"""
        if not output_path:
            ts = time.strftime("%Y%m%d_%H%M%S")
            domain = re.sub(r"https?://(www\.)?", "", url).split("/")[0][:30]
            output_path = str(SCREENSHOT_DIR / f"{domain}_{ts}.png")

        try:
            page = self.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            self._human_delay(0.5, 1.5)
            if kwargs.get("dismiss_cookies", True):
                self._dismiss_cookie_popup(page)
            page.screenshot(path=output_path, full_page=full_page)
            page.close()
            return output_path
        except Exception as e:
            print(f"[BrowserScraper] screenshot 失败: {e}", file=sys.stderr)
            return None

    # ── 交互操作 ─────────────────────────────────────────────

    def click_and_wait(self, url: str, click_selector: str,
                       wait_selector: str = None) -> Optional[str]:
        """点击某元素后等待并返回新页面的 HTML。"""
        try:
            page = self.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            self._dismiss_cookie_popup(page)
            page.click(click_selector, timeout=self.timeout_ms)
            self._human_delay(0.5, 1.5)
            if wait_selector:
                page.wait_for_selector(wait_selector, timeout=self.timeout_ms)
            html = page.content()
            page.close()
            return html
        except Exception as e:
            print(f"[BrowserScraper] click_and_wait 失败: {e}", file=sys.stderr)
            return None

    def type_and_submit(self, url: str, input_selector: str, text: str,
                        submit_selector: str = None) -> Optional[str]:
        """在输入框中输入文本，可选提交。返回操作后页面 HTML。"""
        try:
            page = self.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            self._dismiss_cookie_popup(page)
            page.fill(input_selector, text, timeout=self.timeout_ms)
            self._human_delay(0.3, 0.8)
            if submit_selector:
                page.click(submit_selector, timeout=self.timeout_ms)
                page.wait_for_load_state("domcontentloaded")
            self._human_delay(0.5, 1.0)
            html = page.content()
            page.close()
            return html
        except Exception as e:
            print(f"[BrowserScraper] type_and_submit 失败: {e}", file=sys.stderr)
            return None

    def login_and_fetch(self, url: str, login_url: str,
                        username_sel: str, password_sel: str,
                        submit_sel: str, username: str, password: str,
                        target_selector: str = None) -> Optional[str]:
        """登录流程：先访问登录页填入凭据，再跳转到目标页抓取。"""
        try:
            page = self.new_page()
            # 登录
            page.goto(login_url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            self._human_delay(0.5, 1.0)
            page.fill(username_sel, username, timeout=self.timeout_ms)
            self._human_delay(0.2, 0.5)
            page.fill(password_sel, password, timeout=self.timeout_ms)
            self._human_delay(0.3, 0.8)
            page.click(submit_sel, timeout=self.timeout_ms)
            page.wait_for_load_state("domcontentloaded")
            self._human_delay(1.0, 2.0)
            # 跳转目标页
            page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
            if target_selector:
                page.wait_for_selector(target_selector, timeout=self.timeout_ms)
            html = page.content()
            page.close()
            return html
        except Exception as e:
            print(f"[BrowserScraper] login_and_fetch 失败: {e}", file=sys.stderr)
            return None

    # ── 智能回退 ─────────────────────────────────────────────

    def smart_fetch(self, url: str, html_text: Optional[str] = None,
                    **kwargs) -> Optional[str]:
        """智能抓取：优先用传入的 html_text；失败则启动浏览器。

        这是最推荐的使用方式——先尝试常规 http_utils 爬取，
        返回空时自动调用浏览器 fetch() 兜底。
        """
        if html_text and len(html_text) > 200:
            return html_text
        return self.fetch(url, **kwargs)

    # ── 便捷函数 ─────────────────────────────────────────────

    def fetch_with_screenshot(self, url: str) -> dict:
        """抓取+截图，返回 {html, screenshot_path}。"""
        html = self.fetch(url)
        shot = self.screenshot(url)
        return {"html": html, "screenshot_path": shot}

    # ── 内部辅助 ─────────────────────────────────────────────

    def _dismiss_cookie_popup(self, page: Page):
        """尝试点击页面上的 Cookie 同意按钮。"""
        for selector in COOKIE_CONSENT_SELECTORS:
            try:
                btn = page.query_selector(selector)
                if btn and btn.is_visible():
                    btn.click(timeout=3000)
                    return
            except Exception:
                continue

    def _auto_scroll(self, page: Page, times: int = 5):
        """模拟人工滚动，触发懒加载内容。"""
        for i in range(times):
            page.evaluate(f"window.scrollTo(0, {(i + 1) * 800})")
            self._human_delay(0.3, 0.8)
        # 滚回顶部
        page.evaluate("window.scrollTo(0, 0)")

    @staticmethod
    def _human_delay(min_s: float = 0.1, max_s: float = 0.5):
        """随机延迟，模拟人类浏览速度。"""
        time.sleep(random.uniform(min_s, max_s))


# ── 模块级便捷函数 ──────────────────────────────────────────

def browser_fetch(url: str, headless: bool = False,
                  scroll: bool = False) -> Optional[str]:
    """一行代码启动浏览器抓取。"""
    with BrowserScraper(headless=headless) as bs:
        return bs.fetch(url, scroll=scroll)


def browser_screenshot(url: str, output_path: str = None) -> Optional[str]:
    """一行代码截图。"""
    with BrowserScraper(headless=True) as bs:
        return bs.screenshot(url, output_path)


def smart_fallback(url: str, http_html: Optional[str],
                   headless: bool = False) -> Optional[str]:
    """智能回退：HTTP 返回空 → 浏览器兜底。"""
    if http_html and len(http_html) > 200:
        return http_html
    return browser_fetch(url, headless=headless)


# ── CLI ──────────────────────────────────────────────────────

def main():
    if not PLAYWRIGHT_AVAILABLE:
        print(INSTALL_HINT)
        return

    import argparse
    ap = argparse.ArgumentParser(description="浏览器自动化爬虫")
    ap.add_argument("url", help="目标网址")
    ap.add_argument("--visible", action="store_true", help="可见窗口模式")
    ap.add_argument("--screenshot", action="store_true", help="截图保存")
    ap.add_argument("--scroll", action="store_true", help="自动滚动加载")
    ap.add_argument("--selector", help="提取指定 CSS 选择器的文本")
    ap.add_argument("--wait", help="等待该选择器出现后再提取")
    ap.add_argument("--output", help="HTML 输出文件路径")
    args = ap.parse_args()

    with BrowserScraper(headless=not args.visible) as bs:
        if args.screenshot:
            path = bs.screenshot(args.url)
            print(f"截图: {path}")

        if args.selector:
            text = bs.extract_text(args.url, selector=args.selector,
                                   wait_selector=args.wait,
                                   scroll=args.scroll)
            if text:
                print(text[:2000])
        else:
            html = bs.fetch(args.url, wait_selector=args.wait,
                           scroll=args.scroll)
            if html:
                if args.output:
                    Path(args.output).write_text(html, encoding="utf-8")
                    print(f"已保存: {args.output} ({len(html)} 字符)")
                else:
                    print(f"成功: {len(html)} 字符")
                    # 提取 title
                    m = re.search(r"<title[^>]*>(.*?)</title>", html,
                                  re.IGNORECASE | re.DOTALL)
                    if m:
                        print(f"标题: {m.group(1).strip()[:100]}")
            else:
                print("抓取失败")


if __name__ == "__main__":
    main()
