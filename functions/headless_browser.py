def login(browser, uname, pword):
    username = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_LoginView_LoginControl_UserName"]')
    password = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_LoginView_LoginControl_Password"]')

    username.send_keys(uname)
    password.send_keys(pword)

    login = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_LoginView_LoginControl_LoginButton"]')

    login.click()

def acquire_report(browser, start_date=None):
    from datetime import datetime, timedelta

    if start_date == None:
        # get the date 1 day ago (safest refresh time for )
        start_date = datetime.today() - timedelta(days=1)

    sday = start_date.strftime('%d')
    smonth = start_date.strftime('%m')
    syear = start_date.strftime('%Y')

    start_day = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_startDay"]/option[text()={}]'.format(sday)).click()
    end_day = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_endDay"]/option[text()={}]'.format(sday)).click()

    start_Month = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_startMonth"]/option[text()={}]'.format(smonth)).click()
    end_Month = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_endMonth"]/option[text()={}]'.format(smonth)).click()

    start_Year = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_startYear"]/option[text()={}]'.format(syear)).click()
    end_Year = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_endYear"]/option[text()={}]'.format(syear)).click()

    select_all = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_chkSelectAll"]').click()
    excel_export = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_reportType_1"]').click()

    EXPORT = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_btnGenerateReport"]').click()

    return start_date.strftime('%Y/%m/%d')
