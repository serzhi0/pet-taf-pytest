import pytest
from pytest_html import extras
import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
config_dict = dict(json.load(open('config.json')))
BASE_URL = config_dict['base_url']
TRACE_DIR = f'{config_dict["trace_dir"]}{int(datetime.now().timestamp())}/'


@pytest.fixture(scope='session')
def session_fixture(browser):
    params = config_dict['context_params']
    brow = browser.new_context(**params)
    yield brow
    brow.close()


@pytest.fixture
def function_fixture(session_fixture, request, extra):
    context = session_fixture
    context.tracing.start(screenshots=True, snapshots=True)
    page = context.new_page()
    page.goto(BASE_URL)
    yield page
    status = request.node.rep_call.outcome
    if status == 'failed':
        context.tracing.stop(path=f'{TRACE_DIR}{request.node.name}.zip')
    else:
        context.tracing.stop()


def pytest_html_report_title(report):
    report.title = "My very own title!"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            link = f'https://trace.playwright.dev/?trace={TRACE_DIR}{item.name}.zip'
            extra.append(pytest_html.extras.url(link, name='View Trace'))
        report.extra = extra

# extras.url(f'{item.name}.zip', name='View Trace'))