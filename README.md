# ImageFinder
Finds the images that contains you in it using your given pic


Code Space
---

The `wasteTries` dir consists of all the tries I have made to make it work.

For time beign I have decided to use the `faceMatch.py` as the most effecient way to match the images using `face recognition`.

The `index.py` contains the server side code, and the `database.py` is for managing the database. The database part is in progress.

---
### Avoid `JSON`? 
For now I just decided to use json. But there is another alternative way also to avoid the client side code. That is using `google forms` we can get all the required data in forms along with the images. Then map all the potential datas with the images and match then and then send them.