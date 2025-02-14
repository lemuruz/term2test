from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from mypoll.models import Poll, Choice

class testUserPlayPoll(StaticLiveServerTestCase):
    def setUp(self):
        
        self.poll = Poll.objects.create(name="แมวหรือหมา")
        self.choice1 = Choice.objects.create(poll=self.poll, name="แมว", vote_count=10)
        self.choice2 = Choice.objects.create(poll=self.poll, name="หมา", vote_count=7)

        self.browser = webdriver.Chrome()
    def tearDown(self):
        self.browser.quit()

    def test(self):
        # ปาร์คได้ยินมาจากเพื่อนเรื่องเว็บ polls ปาร์คจึงอยากลองเล่นดู
        # ปาร์คเข้ามาที่หน้าเว็บ
        self.browser.get(self.live_server_url)
        # ปาร์คเห็นลิงิค์ poll อยู่ 1 อันชื่อว่า "แมวหรือหมา"
        cat_or_dog_poll = self.browser.find_element(By.LINK_TEXT, "1. แมวหรือหมา")
        # ปาร์คกดเข้าไปที่ลิงค์
        cat_or_dog_poll.click()
        # ปาร์คเห็นว่ามีปุ่มสองปุ่ม (แมว กับ หมา)
        catBtn = self.browser.find_element(By.ID, "แมว")
        dogBtn = self.browser.find_element(By.ID, "หมา")
        catBtn.is_displayed()
        dogBtn.is_displayed()
        # ปาร์คกด หมา และกด submit
        dogBtn.click()
        self.browser.find_element(By.ID, "Submit Vote").click()
        # ปาร์คเห็นว่า หน้าเว็บเปลี่ยนไปและมีขึ้นว่า แมว => 11 หมา => 8
        catScore = self.browser.find_element(By.ID, "แมว")
        dogScore = self.browser.find_element(By.ID, "หมา")
        self.assertEqual(catScore.text, "แมว (10)")
        self.assertEqual(dogScore.text, "หมา (8)")