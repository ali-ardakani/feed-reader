<div align="center">
<!-- Title: -->
<h1>Feed Reader</h1>
<!-- Description: -->
<p>Feed Reader is a simple RSS reader.</p>
</div>

<!-- Table of Contents: -->
<div align="left">
<h2>Table of Contents</h2>
<ol>
<li><a href="#about">About</a></li>
<li><a href="#getting-started">Getting Started</a></li>
<li><a href="#usage">Usage</a></li>
</ol>

</div>
 
<!-- About: -->
<div align="left">
<h2 id="about">About</h2>
<p>Feed Reader is a simple RSS scraper that allows you to view the latest news from your favorite websites.
After you add a category and a website, you can view and manage your feeds.</p>
<p>The technologies used in this project are:</p>
<ul>
<li>Django</li>
<li>Django Rest Framework</li>
<li>PostgreSQL</li>
<li>Redis</li>
<li>Celery</li>
<li>Docker</li>
<li>Docker Compose</li>
</ul>
</div>
 
<!-- Getting Started: -->
<div align="left">
<h2 id="getting-started">Getting Started</h2>
<p>
<h3>Setup</h3>
<!-- Docker -->
<p>
<h4>Docker</h4>
<ol>
<li>Install Docker</li>
<li>Clone the repository</li>
<li>Run the following command in the root directory of the project: <code>docker-compose up --build</code></li>
</ol>

</p>
<!-- Usage: -->
<div align="left">
<h2 id="usage">Usage</h2>
<p>
<h3>API</h3>
<p>
<h3>Sample Requests</h3>
<p>
<h4>Register</h4>

```bash
curl --location --request POST 'http://localhost:8000/api/user/register/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "test",
    "password": "test",
    "email": "test@test.com"
}'
```

<!-- Response -->

```json
{ "id": 1, "username": "test", "email": "test@test.com" }
```

</p>
<p>
<h4>Login</h4>

```bash
curl --location --request POST 'http://localhost:8000/api/user/login/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "username": "test",
    "password": "test"
}'
```

<!-- Response -->

```json
{
  "token": "your-token",
  "username": "test",
  "email": "test@test.com"
}
```

</p>
<p>
<h4>Create Category</h4>

```bash
curl --location --request POST 'http://localhost:8000/api/category/create/' \
--header 'Authorization: Token your-token' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Technology",
    "source": [1]
}'
```

<!-- Response -->

```json
{"name":"Technology","source":[1]}
```

</p>

<h4>Category List</h4>

```bash
curl --location --request GET 'http://localhost:8000/api/category/list/' \
--header 'Authorization: Token your-token'
```

```json
{"count":1,"next":null,"previous":null,"results":[{"name":"Technology","source":[1]}]}
```

<h4>Get Category</h4>

```bash
curl --location --request GET 'http://localhost:8000/api/category/1/' \
--header 'Authorization: Token your-token'
```

```json
{"name":"Technology","source":[1]}
```


<h4>Get Feeds</h4>

```bash
curl --location --request GET 'http://localhost:8000/api/feed/list/' \
--header 'Authorization: Token your-token'
```

<!-- Response -->

```json
{"count":1,"next":null,"previous":null,"results":[{"author":"test","title":"test","link":"test.com","published":"2022-05-15T17:29:35Z","updated":"2022-05-15T17:29:35Z","categories":["Technology"],"bookmarked":false}]}
```
<p>You can also set the <code>bookmark</code> parameter to <code>true</code> to get only the bookmarked feeds.and set the <code>category</code> parameter to get feeds from a specific category.</p>
example:

```bash
curl --location --request GET 'http://localhost:8000/api/feed/list/?bookmark=false&category=Technology' \
--header 'Authorization: Token your-token'
```
 
</p>

<h4>Get Feed</h4>

```bash
curl --location --request GET 'http://localhost:8000/api/feed/1/' \
--header 'Authorization: Token your-token'
```

```json
{"author":"test","title":"test","link":"test.com","published":"2022-05-15T17:29:35Z","updated":"2022-05-15T17:29:35Z","categories":["test"],"bookmarked":false}
```
</p>

<h4>Bookmark Feed</h4>

```bash
curl --location --request POST 'http://localhost:8000/api/feed/1/bookmark/' \
--header 'Authorization: Token your-token'
```

```json
{"author":"test","title":"test","link":"test.com","published":"2022-05-15T17:29:35Z","updated":"2022-05-15T17:29:35Z","categories":["Technology"],"bookmarked":true}
```
 
</p>
<h4>Unbookmark Feed</h4>

```bash
curl --location --request POST 'http://localhost:8000/api/feed/1/bookmark/' \
--header 'Authorization: Token your-token'
```

```json
{"author":"test","title":"test","link":"test.com","published":"2022-05-15T17:29:35Z","updated":"2022-05-15T17:29:35Z","categories":["Technology"],"bookmarked":false}
```

</p>

</div>
 
<!-- Notes: -->
<div align="left">
<h2>Notes</h2>
<p>
<h3>TESTING</h3>
<p>
<h4>Run Tests</h4>
Note: After the application is running, run the following command in a new terminal window:
  
  ```bash
  docker-compose exec web python manage.py test
  ```
</p>
</div>
