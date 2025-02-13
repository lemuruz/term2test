from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class testUserPlayPoll(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self):
        self.browser.quit()

    def test(self):
        # ปาร์คได้ยินมาจากเพื่อนเรื่องเว็บ polls ปาร์คจึงอยากลองเล่นดู
        # ปาร์คเข้ามาที่หน้าเว็บ
        self.browser.get(self.live_server_url)
        # ปาร์คเห็นลิงิค์ poll อยู่ 1 อันชื่อว่า "แมวหรือหมา"
        cat_or_dog_poll = self.browser.find_element(By.ID, "cat_or_dog_poll")
        # ปาร์คกดเข้าไปที่ลิงค์
        cat_or_dog_poll.click()
        # ปาร์คเห็นว่ามีปุ่มสองปุ่ม (แมว กับ หมา)
        catBtn = self.browser.find_element(By.ID, "catBtn")
        dogBtn = self.browser.find_element(By.ID, "dogBtn")
        catBtn.is_displayed()
        dogBtn.is_displayed()
        # ปาร์คกด หมา
        dogBtn.click()
        # ปาร์คเห็นว่า หน้าเว็บเปลี่ยนไปและมีขึ้นว่า แมว => 11 หมา => 8
        catScore = self.browser.find_element(By.ID, "cat")
        dogScore = self.browser.find_element(By.ID, "dog")
        self.assertEqual(catScore.text, "11")
        # self.assertEqual(dogScore.text, "8")