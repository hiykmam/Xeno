from tortoise import fields,models

#レートが500未満を、早苗
#レートが500を超えたら、霊峰
#レートが1800を超えたら、神威
#とクラス分けする。

class user(models.Model):
    id = fields.IntField(pk = True)
    user_id = fields.CharField(max_length=16,unique=True)
    password_hash = fields.CharField(max_length=128)
    display_name = fields.CharField(max_length=50)

    total_wins = fields.IntField(default=0)
    total_games = fields.IntField(default=0)
    recent_histiry = fields.SmallIntField(default=0)
    rate = fields.BigIntField(default=0)

    class Meta:
        table = "users"

    def __str__(self):
        return self.display_name
    
    async def win(self):
        self.total_games +=1
        self.total_wins  +=1
        self.recent_histiry = ((self.recent_histiry<<1)|1)&0x7FFF
        self.rate = self.reating
        await self.save()
    
    async def lose(self):
        self.total_games +=1
        self.recent_histiry = ((self.recent_histiry<<1)|0)&0x7FFF
        self.rate = self.reating
        await self.save()

    @property
    def is_rank_visible(self):
        return self.total_games >= 15
    
    @property
    def reating(self):
        recent_wins = bin(self.recent_histiry).count('1')
        burst =  recent_wins << 6
        career_base = self.total_wins >> 3
        win_factor = max(1,recent_wins)
        stability = career_base * win_factor
        return burst + stability

