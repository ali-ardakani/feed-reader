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
<p>Feed Reader is a simple RSS reader. It is a simple project made using Django and Django Rest Framework.</p></br>
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
  "token": "e48a46ef000666a6e6ec88576fbb04c95e70c5b5",
  "username": "test",
  "email": "test@test.com"
}
```

</p>
<p>
<h4>Create Feed</h4>

```bash
curl --location --request POST 'http://localhost:8000/api/feed/create/' \
--header 'Authorization: Token 1d784e5f084bdcb39e228dc5a1c319d0c510e0f0' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Test Feed"
}'
```

<!-- Response -->

```json
{ "user": "test", "title": "Test Feed", "bookmarked": false }
```

</p>

<h4>Get Feeds</h4>

```bash
curl --location --request GET 'http://localhost:8000/api/feed/' \
--header 'Authorization: Token 1d784e5f084bdcb39e228dc5a1c319d0c510e0f0'
```

<!-- Response -->

```json
[{ "user": "test", "title": "Test Feed", "bookmarked": false }]
```

</p>

<h4>Get Feed</h4>

```bash
curl --location --request GET 'http://localhost:8000/api/feed/1/' \
--header 'Authorization: Token e48a46ef000666a6e6ec88576fbb04c95e70c5b5'
```

```json
{ "user": "test", "title": "Test Feed", "bookmarked": false }
```
</p>
<h4>Update Feed</h4>

```bash
curl --location --request PUT 'http://localhost:8000/api/feed/1/' \
--header 'Authorization: Token e48a46ef000666a6e6ec88576fbb04c95e70c5b5' \
--header 'Content-Type: application/json' \
--data-raw '{
    "title": "Test Feed Updated"
}'
```

Note: The update is done in async using celery. The feed will be updated after a few seconds.

</p>

<h4>Delete Feed</h4>

```bash
curl --location --request DELETE 'http://localhost:8000/api/feed/1/' \
--header 'Authorization: Token e48a46ef000666a6e6ec88576fbb04c95e70c5b5'
```

```json
{ "user": "test", "title": "Test Feed", "bookmarked": false }
```

</p>

<h4>Bookmark Feed</h4>

```bash
curl --location --request POST 'http://localhost:8000/api/feed/1/bookmark/' \
--header 'Authorization: Token e48a46ef000666a6e6ec88576fbb04c95e70c5b5'
```

```json
{ "user": "test", "title": "Test Feed", "bookmarked": true }
```
 
</p>
<h4>Unbookmark Feed</h4>

```bash
curl --location --request POST 'http://localhost:8000/api/feed/1/bookmark/' \
--header 'Authorization: Token e48a46ef000666a6e6ec88576fbb04c95e70c5b5'
```

```json
{ "user": "test", "title": "Test Feed", "bookmarked": false }
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
