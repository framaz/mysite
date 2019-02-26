from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Game(models.Model):
    x_user = models.ForeignKey('auth.User',on_delete=models.CASCADE,null=True, related_name="user_x_of_ticgame")
    o_user = models.ForeignKey('auth.User',on_delete=models.CASCADE,null=True, related_name="user_y_of_ticgame")
    hoster = models.ForeignKey('auth.User',on_delete=models.CASCADE, related_name="hoster_of_ticgame")
    game = models.CharField(max_length=9,default="")
    is_ended = models.BooleanField(default=False)
    
    def get_classic(self):
        result = [["","",""],["","",""],["","",""]]
        side_flipper = 0
        for i in self.game:
            c=int(i)
            if side_flipper == 0:
                result[int(c/3)][int(c%3)] = '0'
            else:
                result[int(c/3)][int(c%3)] = '1'
            side_flipper =(side_flipper+1)%2
        return result
    def check_for_win(self):
        result = self.get_classic()
        x_counter_vert = 0
        o_counter_vert = 0
        x_counter_hor = 0
        o_counter_hor = 0
        print(result)
        for i in [0,1,2]:
            x_counter_vert = 0
            o_counter_vert = 0
            x_counter_hor = 0
            o_counter_hor = 0
            for j in [0,1,2]:
                if result[i][j] == "0":
                    x_counter_vert+=1
                if result[i][j] == "1":
                    o_counter_vert+=1
                if result[j][i] == "0":
                    x_counter_hor+=1
                if result[j][i] == "1":
                    o_counter_hor+=1
            if(x_counter_vert == 3 or x_counter_hor == 3):
                self.is_ended = True
                return 'x'
            if(o_counter_vert == 3 or o_counter_hor == 3):
                self.is_ended = True
                return 'o'
        if len(self.game) == 9:
            self.is_ended = True
            return 'z'
            
        return 'n'