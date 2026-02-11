# API 用例快速转换模板（精简版）

每个用例只需填写 4 项核心信息，复制粘贴即可。

---

## 用例 1: 管理后台正常创建学员

**用例 ID**: 1150695810001062388

**cURL**:
```bash
curl 'http://i.edu.fkw.com.faidev.cc/ajax/eduStudent_h.jsp?cmd=addEduStudentAndAcct&_TOKEN=680296897df87a74754e1e352e31b7bd&wxappAid=3444128&wxappId=110' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  --data-raw 'propList=%5B%7B%22v%22%3A%22km0210%22%2C%22p%22%3A2%7D%2C%7B%22v%22%3A%22%22%2C%22p%22%3A10%7D%2C%7B%22v%22%3A%22%22%2C%22p%22%3A3%7D%2C%7B%22v%22%3A%22%22%2C%22p%22%3A10002%7D%2C%7B%22v%22%3A%22%22%2C%22p%22%3A10001%7D%2C%7B%22v%22%3A%22%22%2C%22p%22%3A5%7D%2C%7B%22v%22%3A%220%22%2C%22p%22%3A4%7D%2C%7B%22v%22%3A%22%22%2C%22p%22%3A9%7D%2C%7B%22v%22%3A%22%22%2C%22p%22%3A500%7D%2C%7B%22v%22%3A%22%22%2C%22p%22%3A6%7D%2C%7B%22v%22%3A%22%22%2C%22p%22%3A10003%7D%2C%7B%22v%22%3A%22%22%2C%22p%22%3A10004%7D%5D&photoImg=&schoolManagerTeacherIdList=%5B%5D&acct=km0210&pwd=e10adc3949ba59abbe56e057f20f883e&pwdCheck=e10adc3949ba59abbe56e057f20f883e' \
  --insecure
```

**验证条件**:
```
success = true
id 存在
```

**动态字段**: name → `接口测试音频_{timestamp}`

---

## 用例 2: 管理后台正常创建线下课程

**用例 ID**: 1150695810001062389

**cURL**:
```bash
curl 'http://i.edu.fkw.com.faidev.cc/ajax/eduCourse_h.jsp?cmd=addCourse&_TOKEN=680296897df87a74754e1e352e31b7bd&wxappAid=3444128&wxappId=110' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --data-raw 'courseType=0&courseName=km%E7%BA%BF%E4%B8%8B%E8%AF%BE111&tollMethod=0&purchaseLimit=false&content=&summary=&setting=%7B%22bp%22%3A0%2C%22bml%22%3A0%2C%22fdl%22%3A%7B%22s%22%3A0%2C%22ip%22%3A0%2C%22fil%22%3A%5B%5D%2C%22viewType%22%3A0%7D%2C%22btype%22%3A0%2C%22bmtgs%22%3A%5B%5D%2C%22vc%22%3A%7B%22cm%22%3A0%2C%22dd%22%3A%22%22%2C%22du%22%3A0%2C%22et%22%3A0%2C%22vst%22%3A%22%22%2C%22vet%22%3A%22%22%7D%2C%22pageSetting%22%3A%7B%22promptValue%22%3A3%2C%22promptText%22%3A%22%E5%8F%AF%E5%9C%A8%E3%80%90%E6%88%91%E7%9A%84%E3%80%91%E9%A1%B5%E9%9D%A2%EF%BC%8C%E7%82%B9%E5%87%BB%E3%80%90%E6%88%91%E7%9A%84%E8%AF%BE%E7%A8%8B%E3%80%91%E6%9F%A5%E7%9C%8B%E5%B7%B2%E8%B4%AD%E8%AF%BE%E7%A8%8B%22%2C%22jumpValue%22%3A3%2C%22jumpCustomValue%22%3A%5B2%2C3%5D%2C%22customerValue%22%3A3%2C%22guideText%22%3A%22%E5%A6%82%E6%9C%89%E7%96%91%E6%83%91%EF%BC%8C%E5%8F%AF%E9%80%9A%E8%BF%87%E4%BB%A5%E4%B8%8B%E6%96%B9%E5%BC%8F%EF%BC%8C%E4%B8%8E%E6%88%91%E4%BB%AC%E8%81%94%E7%B3%BB%22%2C%22openPhone%22%3Afalse%2C%22phone%22%3A%22%22%2C%22openQrCode%22%3Afalse%2C%22qrCode%22%3A%22%22%2C%22qrCodeUrl%22%3A%22%22%2C%22qrText%22%3A%22%E6%B7%BB%E5%8A%A0%E5%AE%A2%E6%9C%8D%E5%BE%AE%E4%BF%A1%EF%BC%8C%E7%AC%AC%E4%B8%80%E6%97%B6%E9%97%B4%E8%A7%A3%E5%86%B3%E6%82%A8%E7%9A%84%E7%96%91%E9%97%AE%22%2C%22openOfficialCode%22%3Afalse%2C%22officialCode%22%3A%22%22%2C%22officialCodeUrl%22%3A%22%22%2C%22officialText%22%3A%22%E5%85%B3%E6%B3%A8%E5%85%AC%E4%BC%97%E5%8F%B7%EF%BC%8C%E8%8E%B7%E5%8F%96%E6%9C%80%E6%96%B0%E8%AF%BE%E7%A8%8B%E4%BF%A1%E6%81%AF%26%E8%81%94%E7%B3%BB%E5%AE%A2%E6%9C%8D%22%7D%2C%22obsd%22%3A0%2C%22oasd%22%3A0%2C%22bsdd%22%3A%7B%22qrCodeUrl%22%3A%22%22%2C%22qrCode%22%3A%22%22%2C%22eg%22%3A%22%E6%B7%BB%E5%8A%A0%E8%80%81%E5%B8%88%E5%BE%AE%E4%BF%A1%EF%BC%8C%E8%8E%B7%E5%8F%96%E6%9B%B4%E5%A4%9A%E6%9C%8D%E5%8A%A1%22%2C%22wt%22%3A%22%E5%BE%AE%E4%BF%A1%E4%BA%8C%E7%BB%B4%E7%A0%81%22%2C%22wd%22%3A%22%E9%95%BF%E6%8C%89%E4%BA%8C%E7%BB%B4%E7%A0%81%E6%B7%BB%E5%8A%A0%E5%BE%AE%E4%BF%A1%22%2C%22apuw%22%3Afalse%2C%22ep%22%3A0%2C%22bt%22%3A%22%E8%BF%9B%E7%BE%A4%22%7D%2C%22asdd%22%3A%7B%22qrCodeUrl%22%3A%22%22%2C%22qrCode%22%3A%22%22%2C%22eg%22%3A%22%E6%B7%BB%E5%8A%A0%E7%8F%AD%E4%B8%BB%E4%BB%BB%E5%AE%89%E6%8E%92%E8%AF%BE%E7%A8%8B%22%2C%22wt%22%3A%22%E5%BE%AE%E4%BF%A1%E4%BA%8C%E7%BB%B4%E7%A0%81%22%2C%22wd%22%3A%22%E9%95%BF%E6%8C%89%E4%BA%8C%E7%BB%B4%E7%A0%81%E6%B7%BB%E5%8A%A0%E5%BE%AE%E4%BF%A1%22%2C%22apuw%22%3Atrue%2C%22bt%22%3A%22%E6%89%AB%E7%A0%81%22%2C%22ep%22%3A0%7D%2C%22independentOrderProp%22%3Afalse%7D&classifyIdList=%5B%5D&picList=%5B%7B%22id%22%3A%22AJQBCAAQAhgAILqSoMkGKOnJ_o4GMLgIOLgI%22%2C%22url%22%3A%22%2F%2F3444128.s148i.faieduusr.com.faidev.cc%2F2%2F110%2FAJQBCAAQAhgAILqSoMkGKOnJ_o4GMLgIOLgI.jpg%22%7D%5D&addSpecificationList=%5B%7B%22name%22%3A%22100%E8%AF%BE%E6%97%B6%22%2C%22num%22%3A100%2C%22price%22%3A100%2C%22promotionPrice%22%3A50%2C%22total%22%3A1000%2C%22type%22%3A0%2C%22isEdited%22%3Atrue%7D%5D&headerImgList%5B0%5D%5Bid%5D=AJQBCAAQAhgAILqSoMkGKOnJ_o4GMLgIOLgI&headerImgList%5B0%5D%5Burl%5D=%2F%2F3444128.s148i.faieduusr.com.faidev.cc%2F2%2F110%2FAJQBCAAQAhgAILqSoMkGKOnJ_o4GMLgIOLgI.jpg&pl=%7B%22k%22%3A0%2C%22ln%22%3A1%7D&openPresent=false&teachCourseIdList=%5B%5D&isCusAgreement=false&isOpenAgreement=false&agreementId=0&agreementName=&globalAgreement%5Bopen%5D=false&globalAgreement%5Bid%5D=162&globalAgreement%5Bname%5D=%E8%B4%AD%E8%AF%BE%E9%A1%BB%E7%9F%A5&wxappId=110&independentOrderProp=false' \
  --insecure
```

**验证条件**:
```
[例如: success = true, data.id 存在]
```

**动态字段**: [例如: title → `测试标题_{timestamp}`]

---

## 用例 3: 管理后台正常添加系列课

**用例 ID**: 1150695810001062390

**cURL**:
```bash
curl 'http://i.edu.fkw.com.faidev.cc/ajax/wxAppColumn_h.jsp?_TOKEN=680296897df87a74754e1e352e31b7bd&wxappAid=3444128&wxappId=110' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --data-raw 'cmd=addColumn&wxappId=110&name=km%E7%B3%BB%E5%88%97%E8%AF%BE222&summary=&picIdList=%5B%22AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI%22%5D&payModel=1&price=0.01&status=0&introduce=&setting=%7B%22so%22%3A0%2C%22vo%22%3A0%2C%22bp%22%3A0%2C%22bml%22%3A1%2C%22sm%22%3A0%2C%22ds%22%3A0%2C%22btype%22%3A0%2C%22bmtgs%22%3A%5B%5D%2C%22snt%22%3A1%2C%22vct%22%3A1%2C%22utt%22%3A2%2C%22duration%22%3A0%2C%22asp%22%3A0%2C%22lp%22%3A0.01%2C%22slp%22%3A0%2C%22obsd%22%3A0%2C%22oasd%22%3A0%2C%22hd%22%3A0%2C%22bsdd%22%3A%7B%22qrCodeUrl%22%3A%22%22%2C%22qrCode%22%3A%22%22%2C%22eg%22%3A%22%E6%B7%BB%E5%8A%A0%E8%80%81%E5%B8%88%E5%BE%AE%E4%BF%A1%EF%BC%8C%E8%8E%B7%E5%8F%96%E6%9B%B4%E5%A4%9A%E6%9C%8D%E5%8A%A1%22%2C%22wt%22%3A%22%E5%BE%AE%E4%BF%A1%E4%BA%8C%E7%BB%B4%E7%A0%81%22%2C%22wd%22%3A%22%E9%95%BF%E6%8C%89%E4%BA%8C%E7%BB%B4%E7%A0%81%E6%B7%BB%E5%8A%A0%E5%BE%AE%E4%BF%A1%22%2C%22apuw%22%3Afalse%7D%2C%22asdd%22%3A%7B%22qrCodeUrl%22%3A%22%22%2C%22qrCode%22%3A%22%22%2C%22eg%22%3A%22%E6%B7%BB%E5%8A%A0%E8%80%81%E5%B8%88%E5%BE%AE%E4%BF%A1%EF%BC%8C%E8%8E%B7%E5%8F%96%E6%9B%B4%E5%A4%9A%E6%9C%8D%E5%8A%A1%22%2C%22wt%22%3A%22%E5%BE%AE%E4%BF%A1%E4%BA%8C%E7%BB%B4%E7%A0%81%22%2C%22wd%22%3A%22%E9%95%BF%E6%8C%89%E4%BA%8C%E7%BB%B4%E7%A0%81%E6%B7%BB%E5%8A%A0%E5%BE%AE%E4%BF%A1%22%2C%22apuw%22%3Afalse%7D%2C%22stmo%22%3A0%2C%22apl%22%3A%7B%22painlt%22%3A0%2C%22esinlt%22%3A0%7D%2C%22dds%22%3A0%2C%22dateModeDetail%22%3A%7B%22type%22%3A1%2C%22day%22%3A1%2C%22time%22%3A%2208%3A00%22%2C%22num%22%3A1%2C%22itemType%22%3A3%7D%2C%22columnDirectoryStyle%22%3A1%2C%22validityType%22%3A0%2C%22validityDate%22%3A%222026-02-11%22%2C%22fdl%22%3A%7B%22s%22%3A0%2C%22ip%22%3A0%2C%22fil%22%3A%5B%5D%2C%22viewType%22%3A0%2C%22showTime%22%3A0%7D%7D&isBigColumn=false&openPresent=false&classifyIdList=%5B%5D&courseType=0&startType=0&fixedStartTime=&isSignUpEndTime=false&signUpEndTime=&isCusAgreement=false&isOpenAgreement=false&agreementId=0&agreementName=' \
  --insecure
```

**验证条件**:
```

```

**动态字段**: 

---

填写完成后直接粘贴给我即可！

## 用例 4: 管理后台正常添加视频课程

**用例 ID**: 1150695810001062393

**cURL**:curl 'http://i.edu.fkw.com.faidev.cc/ajax/video_h.jsp?_TOKEN=680296897df87a74754e1e352e31b7bd' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  --data-raw 'cmd=addVideo&wxappId=110&id=0&name=km%E8%A7%86%E9%A2%9122&summary=&type=0&vid=&file=AJQBCAAQOhgAIOa0m74GKK7W_8gCMAA4AA&postFile=&classifyIdList=%5B%5D&content=&offSale=false&setting=%7B%22bp%22%3A0%2C%22bml%22%3A1%2C%22btype%22%3A0%2C%22bmtgs%22%3A%5B%5D%2C%22pfk%22%3A%7B%22ss%22%3Afalse%2C%22pm%22%3A0%2C%22pa%22%3A0.01%2C%22sst%22%3A0%2C%22vsu%22%3A0%2C%22atm%22%3A0%2C%22duration%22%3A0%2C%22asp%22%3A0%2C%22lp%22%3A0.01%2C%22slp%22%3A0%2C%22validityType%22%3A0%2C%22validityDate%22%3A%222026-02-11%22%7D%2C%22fdl%22%3A%7B%22s%22%3A0%2C%22ip%22%3A0%2C%22fil%22%3A%5B%5D%2C%22viewType%22%3A0%7D%7D&subscriptionsNum=0&homeworkId=0&columnItemId=0&isRelevancyColumn=false&relevancyColumnId=0&coverType=2&isCusAgreement=false&isOpenAgreement=false&agreementId=0&agreementName=' \
  --insecure


  ## 用例 5: 管理后台正常添加电子书

**用例 ID**: 1150695810001062394

**cURL**:curl 'http://i.edu.fkw.com.faidev.cc/api/manage/electronicBook/addElectronicBook?_TOKEN=680296897df87a74754e1e352e31b7bd&wxappAid=3444128&wxappId=110' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --data-raw 'info=%7B%22name%22%3A%22km%E7%94%B5%E5%AD%90%E4%B9%A6%22%2C%22pic%22%3A%22%22%2C%22picUrl%22%3A%22%22%2C%22author%22%3A%22%22%2C%22summary%22%3A%22%22%2C%22fileId%22%3A%22AJQBCAAQPRgAIMDPgMwGKMSu9ogDMAA4AA%22%2C%22content%22%3A%22%22%2C%22setting%22%3A%7B%22bp%22%3A0%2C%22bml%22%3A1%2C%22btype%22%3A0%2C%22bmtgs%22%3A%5B%5D%2C%22ds%22%3A0%2C%22pfk%22%3A%7B%22ss%22%3Atrue%2C%22pm%22%3A0%2C%22pa%22%3A0.01%2C%22duration%22%3A0%2C%22asp%22%3A1%7D%7D%2C%22fileName%22%3A%22final_optimized_text_version.pdf%22%2C%22fileTypeStr%22%3A%22pdf%22%2C%22relevancyColumnId%22%3A0%2C%22isRelevancyColumn%22%3Afalse%2C%22isCusAgreement%22%3Afalse%2C%22isOpenAgreement%22%3Afalse%2C%22agreementId%22%3A0%2C%22agreementName%22%3A%22%22%2C%22globalAgreement%22%3A%7B%22open%22%3Afalse%2C%22id%22%3A163%2C%22name%22%3A%22%E8%B4%AD%E8%AF%BE%E9%A1%BB%E7%9F%A5%22%7D%7D&isCusAgreement=false&isOpenAgreement=false&agreementId=0&agreementName=' \
  --insecure

## 用例 6: 管理后台正常添加课外服务

**用例 ID**: 1150695810001062395

**cURL**:curl 'http://i.edu.fkw.com.faidev.cc/api/manage/book/addBookService?_TOKEN=680296897df87a74754e1e352e31b7bd&wxappAid=3444128&wxappId=110' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  --data-raw 'serviceName=%E8%AF%BE%E5%A4%96%E6%9C%8D%E5%8A%A122&summary=&price=0&promotionPrice=0&picList=%5B%7B%22id%22%3A%22AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI%22%7D%5D&classifyIdList=%5B%5D&content=&type=0&addSpecificationList=%5B%5D&isLimit=false&addMappingList=%5B%5D&limitCount=0&setting=%7B%22bp%22%3A0%2C%22bml%22%3A1%2C%22btype%22%3A0%2C%22bmtgs%22%3A%5B%5D%2C%22pu%22%3A%7B%22t%22%3A0%2C%22v%22%3A%22%22%7D%2C%22pl%22%3A%7B%22t%22%3A0%2C%22k%22%3A0%2C%22v%22%3A0%2C%22ti%22%3A%22%22%7D%2C%22fdl%22%3A%7B%22s%22%3A0%2C%22ip%22%3A0%2C%22fil%22%3A%5B%5D%2C%22viewType%22%3A0%7D%2C%22cs%22%3A%7B%22p%22%3A%2213919161913%22%2C%22po%22%3Atrue%2C%22prov%22%3A%22%E5%B9%BF%E5%B7%9E%E5%B8%82%22%2C%22addr%22%3A%22%E5%A4%A9%E6%B2%B3%E8%B7%AF250%E5%8F%B7%22%2C%22ao%22%3Afalse%2C%22lat%22%3A0%2C%22lng%22%3A0%2C%22blat%22%3A0%2C%22blng%22%3A0%2C%22bts%22%3A%7B%22odl%22%3A%5B1%2C2%2C3%2C4%2C5%2C6%2C0%5D%2C%22og%22%3A%7B%22t%22%3A0%2C%22gd%22%3A7%7D%2C%22a%22%3A1%2C%22ot%22%3A%7B%22t%22%3A1%2C%22ut%22%3A%5B0%2C1%2C2%2C3%2C4%2C5%2C6%2C23%5D%2C%22ti%22%3A0%2C%22ut30%22%3A%5B0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C45%2C46%2C47%5D%2C%22ut15%22%3A%5B0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C15%2C16%2C17%2C18%2C19%2C20%2C21%2C22%2C23%2C24%2C25%2C26%2C27%2C89%2C90%2C91%2C92%2C93%2C94%2C95%5D%7D%2C%22od%22%3A%7B%22t%22%3A0%2C%22ud%22%3A%5B%5D%2C%22od%22%3A%5B%5D%7D%2C%22lc%22%3A%7B%22c%22%3A1%2C%22l%22%3Atrue%7D%7D%2C%22bto%22%3Afalse%7D%2C%22cso%22%3Afalse%2C%22obsd%22%3A0%2C%22oasd%22%3A0%2C%22bsdd%22%3A%7B%22qrCodeUrl%22%3A%22%22%2C%22qrCode%22%3A%22%22%2C%22eg%22%3A%22%E6%B7%BB%E5%8A%A0%E8%80%81%E5%B8%88%E5%BE%AE%E4%BF%A1%EF%BC%8C%E8%8E%B7%E5%8F%96%E6%9B%B4%E5%A4%9A%E6%9C%8D%E5%8A%A1%22%2C%22wt%22%3A%22%E5%BE%AE%E4%BF%A1%E4%BA%8C%E7%BB%B4%E7%A0%81%22%2C%22wd%22%3A%22%E9%95%BF%E6%8C%89%E4%BA%8C%E7%BB%B4%E7%A0%81%E6%B7%BB%E5%8A%A0%E5%BE%AE%E4%BF%A1%22%2C%22apuw%22%3Afalse%2C%22ep%22%3A0%2C%22bt%22%3A%22%E8%BF%9B%E7%BE%A4%22%7D%2C%22asdd%22%3A%7B%22qrCodeUrl%22%3A%22%22%2C%22qrCode%22%3A%22%22%2C%22eg%22%3A%22%E6%B7%BB%E5%8A%A0%E7%8F%AD%E4%B8%BB%E4%BB%BB%E5%AE%89%E6%8E%92%E8%AF%BE%E7%A8%8B%22%2C%22bt%22%3A%22%E6%89%AB%E7%A0%81%22%2C%22wt%22%3A%22%E5%BE%AE%E4%BF%A1%E4%BA%8C%E7%BB%B4%E7%A0%81%22%2C%22wd%22%3A%22%E9%95%BF%E6%8C%89%E4%BA%8C%E7%BB%B4%E7%A0%81%E6%B7%BB%E5%8A%A0%E5%BE%AE%E4%BF%A1%22%2C%22apuw%22%3Atrue%7D%2C%22ss%22%3A%7B%22pt%22%3A0%2C%22lt%22%3A0%2C%22ct%22%3A0%2C%22so%22%3A%5B%5D%7D%7D&isCusAgreement=false&isOpenAgreement=false&agreementId=0&agreementName=&independentOrderProp=false' \
  --insecure

## 用例 7: 管理后台正常添加实物商品

**用例 ID**: 1150695810001062396

**cURL**:curl 'http://i.edu.fkw.com.faidev.cc/ajax/eduProduct_h.jsp?cmd=addProduct&_TOKEN=680296897df87a74754e1e352e31b7bd&wxappAid=3444128&wxappId=110' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  --data-raw 'name=km%E5%AE%9E%E7%89%A999&remark=&keepProp2=&hasWeight=false&imgList=%5B%22AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI%22%5D&imgPathList=%5B%22%2F%2F3444128.s148i.faieduusr.com.faidev.cc%2F2%2F110%2FAJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI.jpg%22%5D&distributeList=%5B0%2C1%5D&shippingTmpId=-1&specList=%5B%7B%22name%22%3A%22%E5%B0%BA%E7%A0%81%22%2C%22sort%22%3A1%2C%22inPdScValList%22%3A%5B%7B%22fi%22%3A%22%22%2C%22n%22%3A%22s%22%2C%22path%22%3A%22%22%2C%22c%22%3Atrue%7D%2C%7B%22fi%22%3A%22%22%2C%22n%22%3A%22m%22%2C%22path%22%3A%22%22%2C%22c%22%3Atrue%7D%2C%7B%22fi%22%3A%22%22%2C%22n%22%3A%22l%22%2C%22path%22%3A%22%22%2C%22c%22%3Atrue%7D%5D%7D%5D&specInfoList=%5B%7B%22count%22%3A1000%2C%22nameList%22%3A%5B%22s%22%5D%2C%22originPrice%22%3A%221500.00%22%2C%22price%22%3A%22100.00%22%2C%22weight%22%3A%220.00%22%2C%22sort%22%3A1%7D%2C%7B%22count%22%3A1000%2C%22nameList%22%3A%5B%22m%22%5D%2C%22originPrice%22%3A%22257.00%22%2C%22price%22%3A%2217.00%22%2C%22weight%22%3A%220.00%22%2C%22sort%22%3A2%7D%2C%7B%22count%22%3A2000%2C%22nameList%22%3A%5B%22l%22%5D%2C%22originPrice%22%3A%2259.00%22%2C%22price%22%3A%2214.77%22%2C%22weight%22%3A%220.00%22%2C%22sort%22%3A3%7D%5D&setting=%7B%22bp%22%3A0%2C%22bml%22%3A1%2C%22btype%22%3A0%2C%22bmtgs%22%3A%5B%5D%7D&openPresent=false&productOtherSub=0&classifyIdList=%5B%5D&addPresentList=%5B%5D&isCusAgreement=false&isOpenAgreement=false&agreementId=0&agreementName=&independentOrderProp=false&addPropList=%5B%5D&updatePropList=%5B%5D&delPropIdList=%5B%5D' \
  --insecure

## 用例 8: 管理后台正常添加超级题库

**用例 ID**: 1150695810001062397

**cURL**:curl 'http://i.edu.fkw.com.faidev.cc/api/manage/superQuestionBank/addSuperQuestionBank?_TOKEN=680296897df87a74754e1e352e31b7bd&wxappAid=3444128&wxappId=110' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --data-raw 'id=0&name=kmTiku22&summary=&pic=&picUrl=&classifyIdList=%5B%5D&classifyList=%5B%5D&introduce=&payType=3&price=0.01&setting=%7B%22bp%22%3A0%2C%22bml%22%3A1%2C%22btype%22%3A0%2C%22bmtgs%22%3A%5B%5D%2C%22memoryMode%22%3A1%2C%22menuTypes%22%3A%5B1%2C2%2C3%2C4%2C5%5D%2C%22pfk%22%3A%7B%22lp%22%3A0.01%2C%22slp%22%3A0%2C%22duration%22%3A0%2C%22validityType%22%3A0%2C%22asp%22%3A0%2C%22sst%22%3A0%2C%22vsu%22%3A0%2C%22bpam%22%3A1%7D%7D&isCusAgreement=false&isOpenAgreement=false&agreementId=0&agreementName=&globalAgreement=%7B%22open%22%3Afalse%2C%22id%22%3A0%2C%22name%22%3A%22%22%7D' \
  --insecure

## 用例 9: 管理后台正常添加答题活动

**用例 ID**: 1150695810001062398

**cURL**:curl 'http://i.edu.fkw.com.faidev.cc/ajax/wxAppAnswer_h.jsp?cmd=addAnswerActivity&_TOKEN=680296897df87a74754e1e352e31b7bd' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  --data-raw 'isRelevancyColumn=false&relevancyColumnId=0&wxappId=110&isUnLimitTime=true&name=km%E7%AD%94%E9%A2%98&mode=0&startTime=&endTime=&questionBuildAction=0&payType=0&price=0.01&setting=%7B%22at%22%3A%7B%22t%22%3A1%2C%22v%22%3A60%7D%2C%22ac%22%3A%7B%22t%22%3A1%2C%22v%22%3A1%2C%22dailyLimitCount%22%3A1%7D%2C%22pa%22%3A%7B%22t%22%3A0%2C%22v%22%3A%22%22%7D%2C%22bml%22%3A1%2C%22bp%22%3A0%2C%22btype%22%3A0%2C%22bmtgs%22%3A%5B%5D%2C%22wp%22%3A0%2C%22ar%22%3A0%2C%22rqna%22%3Afalse%2C%22wqna%22%3Afalse%2C%22qooo%22%3A0%2C%22memoryMode%22%3A0%2C%22preCheat%22%3A%7B%22cutScreenOpen%22%3Afalse%2C%22cutScreenCount%22%3A3%2C%22cutScreenTime%22%3A3%2C%22screenshotOpen%22%3Afalse%2C%22screenshotCount%22%3A2%2C%22banPasteOpen%22%3Afalse%2C%22noOpsSubOpen%22%3Afalse%2C%22noOpsSubTime%22%3A120%2C%22entriesLimitOpen%22%3Afalse%2C%22entriesCount%22%3A3%2C%22entriesTipsOpen%22%3Afalse%2C%22entriesTxtType%22%3A0%2C%22triggerTipsOpen%22%3Afalse%2C%22triggerType%22%3A0%2C%22triggerTxtType%22%3A0%7D%7D&questionOther=%7B%22st%22%3A%7B%22scs%22%3A1%2C%22cscs%22%3A1%2C%22mcs%22%3A1%2C%22cmcs%22%3A1%2C%22fibs%22%3A1%2C%22cfibs%22%3A1%2C%22tofs%22%3A1%2C%22ctofs%22%3A1%2C%22sas%22%3A1%2C%22csas%22%3A1%2C%22ls%22%3A1%2C%22cls%22%3A1%7D%2C%22questionScoreList%22%3A%5B%5D%2C%22customTypeScoreList%22%3A%5B%5D%7D&classifyIdList=%5B%5D&isCusAgreement=false&isOpenAgreement=false&agreementId=0&agreementName=&version=V2&pic=&questionList=%5B%7B%22id%22%3A77615%2C%22stem%22%3A%22%3Cp%20style%3D%5C%22line-height%3A1.5em%3B%5C%22%3E123%3C%2Fp%3E%22%2C%22type%22%3A0%2C%22content%22%3A%7B%22t%22%3A-1%2C%22ol%22%3A%5B%7B%22id%22%3A1%2C%22v%22%3A%22%3Cp%20style%3D%5C%22line-height%3A1.5em%3B%5C%22%3E12%3C%2Fp%3E%22%2C%22r%22%3Atrue%2C%22picUrl%22%3A%22%22%7D%2C%7B%22id%22%3A2%2C%22v%22%3A%22%3Cp%20style%3D%5C%22line-height%3A1.5em%3B%5C%22%3E434%3C%2Fp%3E%22%2C%22r%22%3Afalse%2C%22picUrl%22%3A%22%22%7D%5D%7D%2C%22answerAnalysis%22%3A%22%22%2C%22groupIdList%22%3A%5B0%5D%2C%22createTime%22%3A1767777575000%2C%22updateTime%22%3A1767777575000%2C%22status%22%3A0%2C%22oldId%22%3A77615%2C%22examSiteIdList%22%3A%5B%5D%2C%22difficulty%22%3A3%2C%22customTypeId%22%3A0%2C%22flag%22%3A0%2C%22customTypeName%22%3A%22%E5%8D%95%E9%80%89%E9%A2%98%22%2C%22snapshot%22%3Afalse%2C%22examSiteInfo%22%3A%5B%5D%2C%22groupInfo%22%3A%5B%7B%22id%22%3A0%2C%22name%22%3A%22%E9%BB%98%E8%AE%A4%E5%88%86%E7%B1%BB%22%7D%5D%2C%22title%22%3A%22123%22%2C%22key%22%3A%2277615%22%7D%2C%7B%22id%22%3A77614%2C%22stem%22%3A%22%3Cp%20style%3D%5C%22line-height%3A1.5em%3B%5C%22%3E11%3C%2Fp%3E%22%2C%22type%22%3A4%2C%22content%22%3A%7B%22p%22%3Afalse%7D%2C%22answerAnalysis%22%3A%22%3Cp%20style%3D%5C%22line-height%3A1.5em%3B%5C%22%3E11%3C%2Fp%3E%22%2C%22groupIdList%22%3A%5B0%5D%2C%22createTime%22%3A1767777567000%2C%22updateTime%22%3A1767777567000%2C%22status%22%3A0%2C%22oldId%22%3A77614%2C%22examSiteIdList%22%3A%5B%5D%2C%22difficulty%22%3A3%2C%22customTypeId%22%3A4%2C%22flag%22%3A0%2C%22customTypeName%22%3A%22%E7%AE%80%E7%AD%94%E9%A2%98%22%2C%22snapshot%22%3Afalse%2C%22examSiteInfo%22%3A%5B%5D%2C%22groupInfo%22%3A%5B%7B%22id%22%3A0%2C%22name%22%3A%22%E9%BB%98%E8%AE%A4%E5%88%86%E7%B1%BB%22%7D%5D%2C%22title%22%3A%2211%22%2C%22key%22%3A%2277614%22%7D%5D' \
  --insecure

## 用例 10: 管理后台正常新建作业

**用例 ID**: 1150695810001062399

**cURL**:curl 'http://i.edu.fkw.com.faidev.cc/ajax/checkpoint_h.jsp?_TOKEN=680296897df87a74754e1e352e31b7bd&wxappAid=3444128&wxappId=110' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --data-raw 'cmd=addCheckpoint&name=%E6%89%93%E5%8D%A1___1&picIdList=%5B%22AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI%22%5D&rule=&payType=0&dailyCount=1&auditType=0&taskCount=3&price=0.1&noticeTime=&isCusAgreement=false&isOpenAgreement=false&agreementId=0&agreementName=&taskList=%5B%7B%22id%22%3A1%2C%22name%22%3A%221%22%2C%22rule%22%3A%22%3Cp%20style%3D%5C%22line-height%3A1.5em%3B%5C%22%3E1%3C%2Fp%3E%22%2C%22sequence%22%3A%2201%22%2C%22dailyCount%22%3A0%2C%22requirement%22%3A%7B%22t%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22i%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22audio%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22video%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22completeQuestion%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22linkQuestion%22%3A%7B%22link%22%3A%5B%5D%2C%22isOpen%22%3Afalse%7D%7D%2C%22passCount%22%3A0%2C%22taskCount%22%3A0%2C%22isNewAdd%22%3Atrue%7D%2C%7B%22id%22%3A2%2C%22name%22%3A%222%22%2C%22rule%22%3A%22%3Cp%20style%3D%5C%22line-height%3A1.5em%3B%5C%22%3E2%3C%2Fp%3E%22%2C%22sequence%22%3A%2202%22%2C%22dailyCount%22%3A0%2C%22requirement%22%3A%7B%22t%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22i%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22audio%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22video%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22completeQuestion%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22linkQuestion%22%3A%7B%22link%22%3A%5B%5D%2C%22isOpen%22%3Afalse%7D%7D%2C%22passCount%22%3A0%2C%22taskCount%22%3A0%2C%22isNewAdd%22%3Atrue%7D%2C%7B%22id%22%3A3%2C%22name%22%3A%223%22%2C%22rule%22%3A%22%3Cp%20style%3D%5C%22line-height%3A1.5em%3B%5C%22%3E3%3C%2Fp%3E%22%2C%22sequence%22%3A%2203%22%2C%22dailyCount%22%3A0%2C%22requirement%22%3A%7B%22t%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22i%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22audio%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22video%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22completeQuestion%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22linkQuestion%22%3A%7B%22link%22%3A%5B%5D%2C%22isOpen%22%3Afalse%7D%7D%2C%22passCount%22%3A0%2C%22taskCount%22%3A0%2C%22isNewAdd%22%3Atrue%7D%5D' \
  --insecure

## 用例 11: 管理后台正常添加打卡活动

**用例 ID**: 1150695810001062400

**cURL**:curl 'http://i.edu.fkw.com.faidev.cc/ajax/checkpoint_h.jsp?_TOKEN=680296897df87a74754e1e352e31b7bd&wxappAid=3444128&wxappId=110' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --data-raw 'cmd=addCheckpoint&name=%E6%89%93%E5%8D%A1___1&picIdList=%5B%22AJQBCAAQAhgAIKWqgMwGKObW7pcGMLgIOLgI%22%5D&rule=&payType=0&dailyCount=1&auditType=0&taskCount=3&price=0.1&noticeTime=&isCusAgreement=false&isOpenAgreement=false&agreementId=0&agreementName=&taskList=%5B%7B%22id%22%3A1%2C%22name%22%3A%221%22%2C%22rule%22%3A%22%3Cp%20style%3D%5C%22line-height%3A1.5em%3B%5C%22%3E1%3C%2Fp%3E%22%2C%22sequence%22%3A%2201%22%2C%22dailyCount%22%3A0%2C%22requirement%22%3A%7B%22t%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22i%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22audio%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22video%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22completeQuestion%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22linkQuestion%22%3A%7B%22link%22%3A%5B%5D%2C%22isOpen%22%3Afalse%7D%7D%2C%22passCount%22%3A0%2C%22taskCount%22%3A0%2C%22isNewAdd%22%3Atrue%7D%2C%7B%22id%22%3A2%2C%22name%22%3A%222%22%2C%22rule%22%3A%22%3Cp%20style%3D%5C%22line-height%3A1.5em%3B%5C%22%3E2%3C%2Fp%3E%22%2C%22sequence%22%3A%2202%22%2C%22dailyCount%22%3A0%2C%22requirement%22%3A%7B%22t%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22i%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22audio%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22video%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22completeQuestion%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22linkQuestion%22%3A%7B%22link%22%3A%5B%5D%2C%22isOpen%22%3Afalse%7D%7D%2C%22passCount%22%3A0%2C%22taskCount%22%3A0%2C%22isNewAdd%22%3Atrue%7D%2C%7B%22id%22%3A3%2C%22name%22%3A%223%22%2C%22rule%22%3A%22%3Cp%20style%3D%5C%22line-height%3A1.5em%3B%5C%22%3E3%3C%2Fp%3E%22%2C%22sequence%22%3A%2203%22%2C%22dailyCount%22%3A0%2C%22requirement%22%3A%7B%22t%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22i%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22audio%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22video%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22completeQuestion%22%3A%7B%22c%22%3Afalse%2C%22mc%22%3A1%7D%2C%22linkQuestion%22%3A%7B%22link%22%3A%5B%5D%2C%22isOpen%22%3Afalse%7D%7D%2C%22passCount%22%3A0%2C%22taskCount%22%3A0%2C%22isNewAdd%22%3Atrue%7D%5D' \
  --insecure

## 用例 12: 管理后台正常添加测评活动

**用例 ID**: 1150695810001062401

**cURL**:curl 'http://i.edu.fkw.com.faidev.cc/api/manage/evaluation/addEvaluation?_TOKEN=680296897df87a74754e1e352e31b7bd&wxappAid=3444128&wxappId=110' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --data-raw 'name=km%E6%B5%8B%E8%AF%84&pic=&picUrl=&summary=&payType=3&payOpportunity=0&price=0.01&introduce=&classifyIdList=%5B%5D&setting=%7B%22bp%22%3A0%2C%22btype%22%3A0%2C%22bmtgs%22%3A%5B%5D%2C%22bml%22%3A1%2C%22pfk%22%3A%7B%22asp%22%3A0%2C%22duration%22%3A0%2C%22validityType%22%3A0%2C%22validityDate%22%3A%22%22%2C%22otc%22%3A0%2C%22stct%22%3A1%2C%22lp%22%3A0.01%2C%22slp%22%3A0%7D%2C%22joinType%22%3A0%2C%22joinNum%22%3A1%2C%22resultType%22%3A0%2C%22resultNum%22%3A1%2C%22dimensionType%22%3A0%2C%22evaluationType%22%3A0%2C%22chartType%22%3A0%2C%22showScore%22%3A1%2C%22showChart%22%3A0%2C%22wxType%22%3A0%2C%22wxDesc%22%3A%22%22%2C%22wxList%22%3A%5B%7B%22open%22%3A0%2C%22qrCode%22%3A%22%22%2C%22text%22%3A%22%22%2C%22qrCodeUrl%22%3A%22%22%7D%2C%7B%22open%22%3A0%2C%22qrCode%22%3A%22%22%2C%22text%22%3A%22%22%2C%22qrCodeUrl%22%3A%22%22%7D%5D%7D&questionSort=%5B-10000001%5D&isCusAgreement=false&isOpenAgreement=false&agreementId=0&agreementName=&globalAgreement=%7B%22open%22%3Afalse%2C%22id%22%3A0%2C%22name%22%3A%22%22%7D&addDimensionList=%5B%5D&addQuestionList=%5B%7B%22id%22%3A-10000001%2C%22stem%22%3A%22111%22%2C%22type%22%3A0%2C%22optionContent%22%3A%7B%22options%22%3A%5B%7B%22id%22%3A1%2C%22value%22%3A%2222%22%2C%22score%22%3A1%7D%2C%7B%22id%22%3A2%2C%22value%22%3A%2233%22%2C%22score%22%3A1%7D%5D%7D%7D%5D&addResultList=%5B%7B%22id%22%3A-1%2C%22name%22%3A%22%E5%85%B6%E4%BB%96%E7%BB%93%E6%9E%9C%22%2C%22section%22%3A%5B%5D%2C%22result%22%3A%22%E6%97%A0%E6%B3%95%E8%AF%84%E4%BC%B0%EF%BC%8C%E8%AF%B7%E9%87%8D%E6%96%B0%E6%B5%8B%E8%AF%95%22%2C%22analysis%22%3A%22%22%2C%22recommend%22%3A%5B%5D%2C%22isOtherResult%22%3Atrue%2C%22setting%22%3A%7B%22rulesType%22%3A0%2C%22cl%22%3A%5B%5D%2C%22so%22%3A0%2C%22sofs%22%3A%5B1%5D%2C%22sd%22%3A1%2C%22sdfs%22%3A%5B1%5D%2C%22sda%22%3A1%7D%7D%5D&addDimensionGroupList=%5B%5D&addOverallIndicatorList=%5B%7B%22id%22%3A-9999%2C%22name%22%3A%22%E6%B5%8B%E8%AF%84%E6%80%BB%E5%88%86%22%2C%22isSys%22%3Atrue%2C%22formula%22%3A%22%23%E6%B5%8B%E8%AF%84%E6%80%BB%E5%88%86%23%22%2C%22isTotalScore%22%3Atrue%2C%22degree%22%3A%7B%22dl%22%3A%5B%5D%7D%7D%2C%7B%22id%22%3A-10000%2C%22name%22%3A%22%E6%B5%8B%E8%AF%84%E5%B9%B3%E5%9D%87%E5%88%86%22%2C%22isSys%22%3Atrue%2C%22formula%22%3A%22%23%E6%B5%8B%E8%AF%84%E5%B9%B3%E5%9D%87%E5%88%86%23%22%2C%22isAverageScore%22%3Atrue%2C%22degree%22%3A%7B%22dl%22%3A%5B%5D%7D%7D%5D&addDimensionIndicatorList=%5B%7B%22id%22%3A-1%2C%22name%22%3A%22%E5%B9%B3%E5%9D%87%E5%88%86%22%2C%22degree%22%3A%7B%22dl%22%3A%5B%5D%7D%2C%22dimensionDegreeList%22%3A%5B%5D%7D%5D' \
  --insecure

  ## 用例 13: 管理后台正常添加表单

**用例 ID**: 1150695810001062402

**cURL**:curl 'http://i.edu.fkw.com.faidev.cc/ajax/wxAppForm_h.jsp?cmd=addWXAppForm&_TOKEN=680296897df87a74754e1e352e31b7bd' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  --data-raw 'name=kmbiaod&contentList=%5B%7B%22name%22%3A%22%E5%8D%95%E8%A1%8C%E6%96%87%E6%9C%AC%22%2C%22type%22%3A0%2C%22placeholder%22%3A%22111%22%2C%22input%22%3A%22%22%2C%22must%22%3Afalse%7D%2C%7B%22name%22%3A%22%E5%8D%95%E9%80%89%E6%8C%89%E9%92%AE%22%2C%22type%22%3A1%2C%22placeholder%22%3A%22%22%2C%22input%22%3A%22%E9%80%89%E9%A1%B9%E4%B8%80%5Cn%E9%80%89%E9%A1%B9%E4%BA%8C%5Cn%E9%80%89%E9%A1%B9%E4%B8%89%22%2C%22must%22%3Afalse%7D%2C%7B%22name%22%3A%22%E5%A4%9A%E9%80%89%E6%8C%89%E9%92%AE%22%2C%22type%22%3A2%2C%22placeholder%22%3A%22%22%2C%22input%22%3A%22%E9%80%89%E9%A1%B9%E4%B8%80%5Cn%E9%80%89%E9%A1%B9%E4%BA%8C%5Cn%E9%80%89%E9%A1%B9%E4%B8%89%22%2C%22must%22%3Afalse%7D%2C%7B%22name%22%3A%22%E5%A4%9A%E8%A1%8C%E6%96%87%E6%9C%AC%22%2C%22type%22%3A3%2C%22placeholder%22%3A%22%22%2C%22input%22%3A%22%22%2C%22must%22%3Afalse%7D%2C%7B%22name%22%3A%22%E6%96%87%E4%BB%B6%E4%B8%8A%E4%BC%A0%22%2C%22type%22%3A4%2C%22placeholder%22%3A%22%22%2C%22input%22%3A%22%22%2C%22fileSetting%22%3A%7B%22fs%22%3A100%2C%22ia%22%3A0%2C%22dftl%22%3A%22%22%2C%22ft%22%3A0%7D%2C%22must%22%3Afalse%7D%2C%7B%22name%22%3A%22%E6%97%A5%E6%9C%9F%E6%97%B6%E9%97%B4%22%2C%22type%22%3A5%2C%22placeholder%22%3A%22%22%2C%22input%22%3A%22%22%2C%22dateSetting%22%3A%7B%22a%22%3A0%2C%22ot%22%3A%7B%22t%22%3A0%2C%22ti%22%3A0%2C%22ut%22%3A%5B0%2C1%2C2%2C3%2C4%2C5%2C6%2C23%5D%2C%22ut15%22%3A%5B0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C14%2C15%2C16%2C17%2C18%2C19%2C20%2C21%2C22%2C23%2C24%2C25%2C26%2C27%2C89%2C90%2C91%2C92%2C93%2C94%2C95%5D%2C%22ut30%22%3A%5B0%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C10%2C11%2C12%2C13%2C45%2C46%2C47%5D%7D%2C%22od%22%3A%7B%22t%22%3A0%2C%22ud%22%3A%5B%5D%2C%22od%22%3A%5B%5D%7D%2C%22ba%22%3Afalse%2C%22bh%22%3Atrue%2C%22bpd%22%3Atrue%7D%2C%22must%22%3Afalse%7D%2C%7B%22name%22%3A%22%E4%B8%8B%E6%8B%89%E9%80%89%E9%A1%B9%22%2C%22type%22%3A7%2C%22placeholder%22%3A%22%22%2C%22input%22%3A%22%E9%80%89%E9%A1%B9%E4%B8%80%5Cn%E9%80%89%E9%A1%B9%E4%BA%8C%5Cn%E9%80%89%E9%A1%B9%E4%B8%89%22%2C%22must%22%3Afalse%7D%2C%7B%22name%22%3A%22%E5%A4%9A%E7%BA%A7%E4%B8%8B%E6%8B%89%22%2C%22type%22%3A20%2C%22placeholder%22%3A%22%22%2C%22input%22%3A%22%22%2C%22multiLevelDropdownSetting%22%3A%7B%22data%22%3A%5B%22%E5%A4%A7%E5%8C%BA%2F%E7%9C%81%E4%BB%BD%2F%E5%9F%8E%E5%B8%82%2F%E5%8C%BA%E5%8E%BF%22%2C%22%E5%8D%8E%E5%8D%97%E5%9C%B0%E5%8C%BA%2F%E5%B9%BF%E4%B8%9C%E7%9C%81%2F%E5%B9%BF%E5%B7%9E%E5%B8%82%2F%E5%A4%A9%E6%B2%B3%E5%8C%BA%22%2C%22%E5%8D%8E%E5%8D%97%E5%9C%B0%E5%8C%BA%2F%E5%B9%BF%E4%B8%9C%E7%9C%81%2F%E5%B9%BF%E5%B7%9E%E5%B8%82%2F%E8%B6%8A%E7%A7%80%E5%8C%BA%22%2C%22%E5%8D%8E%E5%8D%97%E5%9C%B0%E5%8C%BA%2F%E5%B9%BF%E4%B8%9C%E7%9C%81%2F%E5%B9%BF%E5%B7%9E%E5%B8%82%2F%E6%B5%B7%E7%8F%A0%E5%8C%BA%22%2C%22%E5%8D%8E%E5%8D%97%E5%9C%B0%E5%8C%BA%2F%E5%B9%BF%E4%B8%9C%E7%9C%81%2F%E6%B7%B1%E5%9C%B3%E5%B8%82%2F%E5%8D%97%E5%B1%B1%E5%8C%BA%22%2C%22%E5%8D%8E%E5%8D%97%E5%9C%B0%E5%8C%BA%2F%E5%B9%BF%E4%B8%9C%E7%9C%81%2F%E6%B7%B1%E5%9C%B3%E5%B8%82%2F%E7%BD%97%E6%B9%96%E5%8C%BA%22%2C%22%E5%8D%8E%E5%8D%97%E5%9C%B0%E5%8C%BA%2F%E5%B9%BF%E4%B8%9C%E7%9C%81%2F%E6%B7%B1%E5%9C%B3%E5%B8%82%2F%E9%BE%99%E5%8D%8E%E5%8C%BA%22%2C%22%E5%8D%8E%E5%8D%97%E5%9C%B0%E5%8C%BA%2F%E6%B9%96%E5%8D%97%E7%9C%81%2F%E6%A0%AA%E6%B4%B2%E5%B8%82%2F%E8%8A%A6%E6%B7%9E%E5%8C%BA%22%2C%22%E5%8D%8E%E5%8D%97%E5%9C%B0%E5%8C%BA%2F%E6%B9%96%E5%8D%97%E7%9C%81%2F%E9%95%BF%E6%B2%99%E5%B8%82%2F%E5%A4%A9%E5%BF%83%E5%8C%BA%22%2C%22%E5%8D%8E%E4%B8%9C%E5%9C%B0%E5%8C%BA%2F%E4%B8%8A%E6%B5%B7%E5%B8%82%2F%E9%9D%99%E5%AE%89%E5%8C%BA%22%2C%22%E5%8D%8E%E4%B8%9C%E5%9C%B0%E5%8C%BA%2F%E4%B8%8A%E6%B5%B7%E5%B8%82%2F%E9%97%B5%E8%A1%8C%E5%8C%BA%22%2C%22%E5%8D%8E%E4%B8%9C%E5%9C%B0%E5%8C%BA%2F%E6%B5%99%E6%B1%9F%E7%9C%81%2F%E6%9D%AD%E5%B7%9E%E5%B8%82%2F%E6%8B%B1%E5%A2%85%E5%8C%BA%22%2C%22%E5%8D%8E%E4%B8%9C%E5%9C%B0%E5%8C%BA%2F%E6%B5%99%E6%B1%9F%E7%9C%81%2F%E6%9D%AD%E5%B7%9E%E5%B8%82%2F%E4%BD%99%E6%9D%AD%E5%8C%BA%22%2C%22%E5%8D%8E%E5%8C%97%E5%9C%B0%E5%8C%BA%2F%E5%B1%B1%E4%B8%9C%E7%9C%81%2F%E6%B5%8E%E5%8D%97%E5%B8%82%2F%E5%8E%86%E4%B8%8B%E5%8C%BA%22%2C%22%E5%8D%8E%E5%8C%97%E5%9C%B0%E5%8C%BA%2F%E5%B1%B1%E4%B8%9C%E7%9C%81%2F%E6%B5%8E%E5%8D%97%E5%B8%82%2F%E7%AB%A0%E4%B8%98%E5%8C%BA%22%2C%22%E5%8D%8E%E5%8C%97%E5%9C%B0%E5%8C%BA%2F%E5%B1%B1%E4%B8%9C%E7%9C%81%2F%E9%9D%92%E5%B2%9B%E5%B8%82%2F%E9%BB%84%E5%B2%9B%E5%8C%BA%22%2C%22%E5%8D%8E%E5%8C%97%E5%9C%B0%E5%8C%BA%2F%E5%B1%B1%E4%B8%9C%E7%9C%81%2F%E9%9D%92%E5%B2%9B%E5%B8%82%2F%E5%B4%82%E5%B1%B1%E5%8C%BA%22%5D%7D%2C%22must%22%3Afalse%7D%2C%7B%22name%22%3A%22%E7%9C%81%E5%B8%82%E5%8C%BA%E5%8E%BF%22%2C%22type%22%3A8%2C%22placeholder%22%3A%22%22%2C%22input%22%3A%22%22%2C%22addrSetting%22%3A%7B%22p%22%3A%22440000%22%2C%22ph%22%3Afalse%2C%22c%22%3A%22440100%22%2C%22ch%22%3Afalse%2C%22d%22%3A%22440104%22%2C%22dh%22%3Afalse%2C%22a%22%3A%22%E8%AF%B7%E8%BE%93%E5%85%A5%E8%AF%A6%E7%BB%86%E5%9C%B0%E5%9D%8011%22%2C%22ah%22%3Afalse%7D%2C%22must%22%3Afalse%7D%2C%7B%22name%22%3A%22%E9%82%AE%E7%AE%B1%E5%9C%B0%E5%9D%80%22%2C%22type%22%3A10%2C%22placeholder%22%3A%22%22%2C%22input%22%3A%22%22%2C%22must%22%3Afalse%7D%2C%7B%22name%22%3A%22%E8%BA%AB%E4%BB%BD%E8%AF%81%E5%8F%B7%22%2C%22type%22%3A11%2C%22placeholder%22%3A%22%22%2C%22input%22%3A%22%22%2C%22must%22%3Afalse%7D%2C%7B%22name%22%3A%22%E6%89%8B%E6%9C%BA%E5%8F%B7%E7%A0%81%22%2C%22type%22%3A6%2C%22placeholder%22%3A%22%22%2C%22input%22%3A%22%22%2C%22phoneSetting%22%3A%7B%22ov%22%3Afalse%7D%2C%22must%22%3Afalse%7D%5D&wxappId=110&submitCount=0&privacyStatus=true' \
  --insecure

  ## 用例 14: 管理后台正常添加优惠券

**用例 ID**: 1150695810001062403

**cURL**:curl 'http://i.edu.fkw.com.faidev.cc/ajax/coupon_h.jsp?_TOKEN=680296897df87a74754e1e352e31b7bd' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  --data-raw 'wxappId=110&cmd=addCoupon&id=-1&name=km%E4%BC%98%E6%83%A0%E5%88%B8&type=0&discountPrice=100&discount=9.8&timeType=1&startTime=&endTime=&day=1000&remainType=1&remainCount=1&entries=%5B%7B%22type%22%3A5%2C%22selected%22%3Atrue%2C%22name%22%3A%22%E7%B3%BB%E5%88%97%E8%AF%BE%22%2C%22suitableTarget%22%3A%7B%22suitableType%22%3A0%2C%22category%22%3A0%2C%22selectedIdList%22%3A%5B%5D%2C%22selectedClassifyIdList%22%3A%5B%5D%7D%7D%2C%7B%22type%22%3A2%2C%22selected%22%3Atrue%2C%22name%22%3A%22%E9%9F%B3%E9%A2%91%22%2C%22suitableTarget%22%3A%7B%22suitableType%22%3A0%2C%22category%22%3A0%2C%22selectedIdList%22%3A%5B%5D%2C%22selectedClassifyIdList%22%3A%5B%5D%7D%7D%2C%7B%22type%22%3A4%2C%22selected%22%3Atrue%2C%22name%22%3A%22%E8%A7%86%E9%A2%91%22%2C%22suitableTarget%22%3A%7B%22suitableType%22%3A0%2C%22category%22%3A0%2C%22selectedIdList%22%3A%5B%5D%2C%22selectedClassifyIdList%22%3A%5B%5D%7D%7D%2C%7B%22type%22%3A1%2C%22selected%22%3Atrue%2C%22name%22%3A%22%E5%9B%BE%E6%96%87%22%2C%22suitableTarget%22%3A%7B%22suitableType%22%3A0%2C%22category%22%3A0%2C%22selectedIdList%22%3A%5B%5D%2C%22selectedClassifyIdList%22%3A%5B%5D%7D%7D%2C%7B%22type%22%3A0%2C%22selected%22%3Atrue%2C%22name%22%3A%22%E7%BA%BF%E4%B8%8B%E8%AF%BE%E7%A8%8B%22%2C%22suitableTarget%22%3A%7B%22suitableType%22%3A0%2C%22category%22%3A0%2C%22selectedIdList%22%3A%5B%5D%2C%22selectedClassifyIdList%22%3A%5B%5D%7D%7D%2C%7B%22type%22%3A14%2C%22selected%22%3Atrue%2C%22name%22%3A%22%E5%95%86%E5%93%81%22%2C%22suitableTarget%22%3A%7B%22suitableType%22%3A0%2C%22category%22%3A0%2C%22selectedIdList%22%3A%5B%5D%2C%22selectedClassifyIdList%22%3A%5B%5D%7D%7D%2C%7B%22type%22%3A9%2C%22selected%22%3Atrue%2C%22name%22%3A%22%E4%BC%9A%E5%91%98%E5%8D%A1%22%2C%22suitableTarget%22%3A%7B%22suitableType%22%3A0%2C%22category%22%3A0%2C%22selectedIdList%22%3A%5B%5D%2C%22selectedClassifyIdList%22%3A%5B%5D%7D%7D%2C%7B%22type%22%3A7%2C%22selected%22%3Atrue%2C%22name%22%3A%22%E7%AD%94%E9%A2%98%22%2C%22suitableTarget%22%3A%7B%22suitableType%22%3A0%2C%22category%22%3A0%2C%22selectedIdList%22%3A%5B%5D%2C%22selectedClassifyIdList%22%3A%5B%5D%7D%7D%2C%7B%22type%22%3A24%2C%22selected%22%3Atrue%2C%22name%22%3A%22%E6%B5%8B%E8%AF%84%22%2C%22suitableTarget%22%3A%7B%22suitableType%22%3A0%2C%22category%22%3A0%2C%22selectedIdList%22%3A%5B%5D%2C%22selectedClassifyIdList%22%3A%5B%5D%7D%7D%2C%7B%22type%22%3A25%2C%22selected%22%3Atrue%2C%22name%22%3A%22%E9%A2%98%E5%BA%93%22%2C%22suitableTarget%22%3A%7B%22suitableType%22%3A0%2C%22category%22%3A0%2C%22selectedIdList%22%3A%5B%5D%2C%22selectedClassifyIdList%22%3A%5B%5D%7D%7D%2C%7B%22type%22%3A15%2C%22selected%22%3Atrue%2C%22name%22%3A%22%E8%AF%BE%E5%A4%96%E6%9C%8D%E5%8A%A1%22%2C%22suitableTarget%22%3A%7B%22suitableType%22%3A0%2C%22category%22%3A0%2C%22selectedIdList%22%3A%5B%5D%2C%22selectedClassifyIdList%22%3A%5B%5D%7D%7D%5D&rule=&isIntegralMall=false&targetUser=%7B%22bp%22%3A0%2C%22btype%22%3A0%2C%22bmtgs%22%3A%5B%5D%2C%22bml%22%3A1%7D&isNewClassify=true' \
  --insecure

  ## 用例 15: 管理后台正常添加兑换码

**用例 ID**: 1150695810001062404

**cURL**:curl 'http://i.edu.fkw.com.faidev.cc/ajax/eduCouponCode_h.jsp?cmd=addWafCk_saveOrUpdateCoupon&_TOKEN=680296897df87a74754e1e352e31b7bd&wxappAid=3444128&wxappId=110' \
  -H 'Accept: application/json, text/plain, */*' \
  -H 'Accept-Language: zh-CN,zh;q=0.9' \
  -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' \
  -b '_cliid=1T-e9c83fXNN3xzT; loginComeForm=fkjz; wxRegBiz=none; grayUrl=; loginCacct=huaedu1; loginCaid=31687084; loginSacct=boss; loginUseSacct=0; _FSESSIONID=uhbyiwr5X7w3BQRt; loginSign=; _jzmFirstLogin=false; loginTimeInMills=1770779620321; _hasClosePlatinumAd_=false; _hasClosePlatinum_=false; _hasCloseFlyerAd_=false; _hasCloseHdGG_=false; faiscoAd=true; _whereToPortal_=login; _readAllOrderTab=0; _new_reg_home=2; adImg_module_31687084=0_11_1770739200000; _isFirstLoginPc=false; _isFirstLoginPc_7=false; edu_aid=31687084; Hm_lvt_660d2b193b614d425ca241b0f24e5dd4=1770779632; HMACCOUNT=7185220482F3FB3C; todayHasLogin_2=true; JSESSIONID=2687D1AB41EBDB2647B9C7B65E6B56C8; Hm_lpvt_660d2b193b614d425ca241b0f24e5dd4=1770779640; _sid4ue=110' \
  -H 'Origin: http://i.edu.fkw.com.faidev.cc' \
  -H 'Proxy-Connection: keep-alive' \
  -H 'Referer: http://i.edu.fkw.com.faidev.cc/?__aacct=huaedu1' \
  -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36' \
  -H 'X-Requested-With: XMLHttpRequest' \
  --data-raw 'name=km%E5%85%91%E6%8D%A211&channels=%5B%5D&remark=&universalCode=&type=1&codeType=1&generateType=0&startTime=1770181200000&endTime=1803657599000&stockNum=1000&useCount=1&noCountLimit=true&rightsType=1&noTimeLimit=true&couponType=0&savePrice=9.99&saveDiscount=0.1&useStartTime=&useEndTime=&ruleTxt=%E8%AF%B4%E8%AF%B4%E8%AF%B4&pricePageInfo=%7B%22showPrice%22%3A0%2C%22useNotice%22%3A%22%22%7D&isAllCourse=true&serviceList=%5B%5D&serviceInfo=%7B%7D&status=0' \
  --insecure

  ## 用例 16: 

**用例 ID**: 

**cURL**:

  ## 用例 17: 

**用例 ID**: 

**cURL**: