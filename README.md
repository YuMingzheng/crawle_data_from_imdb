# 从IMDB中爬取电影票房信息

IMDB：从这里获取电影信息，电影名称、类型、主演、时长、导演、编剧、出品、发行等

> * url：https://www.imdb.com/title/tt7362036/，可获得：
>
>     1. 电影IMDB编号，例tt7362036
>     2. 电影时长，例1h 57m
>     3. 电影类型，例 Comedy · Drama
>     4. 发行日期，
>     5. 全球总票房，Gross worldwide
>
> * url2：url+"/fullcredits"，可获得：
>
>     1. 导演，例[Muye Wen](https://www.imdb.com/name/nm6337063/?ref_=ttfc_fc_dr1) 
>     2. 编剧，
>     3. 演员表
>
> * url3：url+"/companycredits"，可获得：
>
>     1.  制作公司
>     2.  发行公司
>
> *  对于某一个电影，只获取cast表中的前五个演员的票房、获取所有导演的票房
> 
> * 对于某一个人，只爬取近五年（17-21）的数据
> 
> * 对于某一公司，只爬取近五年的数据（同上
