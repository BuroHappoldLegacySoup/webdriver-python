def login(browser, uname, pword):
    username = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_LoginView_LoginControl_UserName"]')
    password = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_LoginView_LoginControl_Password"]')

    username.send_keys(uname)
    password.send_keys(pword)

    login = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_LoginView_LoginControl_LoginButton"]')

    login.click()

def acquire_report(browser, date=None):

    day = date.strftime('%d')
    month = date.strftime('%m')
    year = date.strftime('%Y')

    start_day = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_startDay"]/option[text()={}]'.format(day)).click()
    end_day = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_endDay"]/option[text()={}]'.format(day)).click()

    start_Month = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_startMonth"]/option[text()={}]'.format(month)).click()
    end_Month = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_endMonth"]/option[text()={}]'.format(month)).click()

    start_Year = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_startYear"]/option[text()={}]'.format(year)).click()
    end_Year = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_endYear"]/option[text()={}]'.format(year)).click()

    select_all = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_chkSelectAll"]').click()
    excel_export = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_reportType_1"]').click()

    EXPORT = browser.find_element_by_xpath('//*[@id="ctl00_MainContent_ReportFilter1_btnGenerateReport"]').click()

    return date.strftime('%Y/%m/%d')
