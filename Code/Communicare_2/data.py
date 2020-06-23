import random
import numpy as np
names = ["Adnan", "Asif", "Ruhama", "Naeem", "Aliza", "Alizaayyyy", "Rafiq", "Batool", "Ahmed", "Yabu",
 "Angel", "Ahmed", "Test", "User", "No", "Name", "xD", "Random"]
xx = "Brock Gale Gustavo Hank Hector Holly Jane Jesse Nadia Mubaraka Bob Marley Marvin Jesse Talha Taha Mr. Mrs. Lydia Marie Mike Pete Saul Skyler Todd Walter Ali Alish Alish Kaisa Nouman Bilal Test2 Test3 Test4 Test4 Test5 Tes7 Test9 Ali Adnan2 Ruhamamammama"
names+= xx.split(" ")

x = "Enter each item on a new line, choose the amount of groups unders settings and click the button to generate your randomized list. Don't like the first team? Just click again until you do. Fairly pick teams without bias No need to draw names out of a hat No need to do a grade school style draft or put hours of thought into the most balanced teams The most fair dividing method possible is random. Mix up your to-do list by generating random groups out of them For example enter all your housecleaning activities and split them into seven groups one for each day or one for each person."
x = x.split()

xxx = "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?"

x+= xxx.split(" ")


print(" ".join(random.choices(names, k=3)))
l = np.random.randn(100)*10

Posts = []
for i in range(120):
    d = {}
    d['author'] = " ".join(random.choices(names, k=2))
    d['Title'] = "Post"+str(i)
    d['Date'] = ''
    d['Content'] = " ".join(random.choices(x, k=14))
    d['Location'] = str(random.choice(l))+","+str(random.choice(l))
    Posts.append(d)

print(Posts[10])