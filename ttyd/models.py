from django.db import models

# 寵寵欲動的功能
class TTYDFunc(models.Model):
    name = models.CharField(max_length=100)    # 功能名稱
    content = models.TextField()			   # 功能內容

class FeedTime(models.Model):
	username = models.CharField(max_length=50)
	feed_time1 = models.TimeField(null=True)
	feed_time2 = models.TimeField(null=True)
	feed_time3 = models.TimeField(null=True)
	pre_feedtime = models.DateTimeField(null=True)
	def __str__(self):
		return self.username