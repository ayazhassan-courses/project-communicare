def calcdist(lat1,lon1,lat2,lon2):
    from math import sin, cos, sqrt, atan2, radians
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    R_earth = 6373.0

    distlat = lat2 - lat1
    distlon = lon2 - lon1


    tval = sin(distlat / 2)**2 + cos(lat1) * cos(lat2) * sin(distlon / 2)**2
    tval2 = 2 * atan2(sqrt(tval), sqrt(1 - tval))

    distance = R_earth * tval2
    return round(distance,2)


def quickSort(lst,col,cond):
    flst = quickSortreal(lst,0,len(lst)-1,col)
    if cond:
        return flst
    else:
        flst.reverse()
        return flst

def quickSortreal(lst,low,high,col):
    if low>=high:
        return 
    else:
        elesort = partition(lst,low,high,col)
        quickSortreal(lst,low,elesort[1],col)
        quickSortreal(lst,elesort[0],high,col)
        return lst
 
def partition(lst,low,high,col):
    mid = (low+high)//2
    pivot = lst[mid] 
    i = low
    j = high

    while(j>=i):
        while(lst[i][col]<pivot[col]):
            i+=1
        while(lst[j][col]>pivot[col]):
            j-=1
        if i<=j:
            lst[i], lst[j] = lst[j] , lst[i]
            i+=1
            j-=1

    return (i,j) 


def sort_locations(db, sortwrt):
    tvalwrt = sortwrt['location'].split(',')
    tlst = []
    flst=[]
    for post in range(len(database)):
        tval = database[post]['location'].split(',')
        distance = calcdist(tvalwrt[0],tvalwrt[1],tval[0],tval[1])
        tlst.append((post,distance))
    
    column = 1
    ascending = True
    sortedlst = quickSort(tlst, column, ascending)
    for fpost in sortedlst:
        flst.append(database[fpost[0]])
    return flst 

    




database = [{'author':'Ruhama','title':'my new post','content':'my name is Ruhama','Date':'2-3-2020','location':'23.656434,24.5454234' },{'author':'Mubaraka','title':'my new post','content':'my name is Ruhama','Date':'2-3-2020','location':'35.653434,91.5434234' },{'author':'Batool','title':'my new post','content':'my name is Ruhama','Date':'2-3-2020','location':'87.243434,35.456434' },{'author':'Adnan','title':'my new post','content':'my name is Ruhama','Date':'2-3-2020','location':'87.609434,43.543544' },{'author':'Fizza','title':'my new post','content':'my name is Ruhama','Date':'2-3-2020','location':'39.986434,43.345234' },]
sortwrt = {'author':'Aliza','title':'my new post','content':'my name is Ruhama','Date':'2-3-2020','location':'56.556434,67.5454234' }

sortedDB = sort_locations(database,sortwrt)
print(sortedDB)
