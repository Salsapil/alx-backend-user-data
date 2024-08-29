# What is PII?
- **Personally Identifiable Information (PII)** refers to any data that can identify a specific individual. It’s sensitive information that should be protected to maintain privacy and security. Protecting PII is crucial to prevent identity theft, fraud, and unauthorized access to personal data.   

# How to implement a log filter that will obfuscate PII fields
## What is Log Filtering?
The process of modifying logs to protect this sensitive information.

### How to Obfuscate PII Fields:
Obfuscation means hiding or masking the actual data. Like replacing an email or password with "***".   

### Steps to Implement a Log Filter:   
**1- Identify PII Fields:** Determine which fields contain PII (like email, password).   
**2- Apply Regex or Similar Techniques:** Use regular expressions (regex) or specific algorithms to find and replace sensitive information in the logs.   
**3- Substitute the PII:** Replace the actual values with a placeholder like *** or REDACTED.   

# How to encrypt a password and check the validity of an input password
## Password Encryption vs. Hashing:
- **Encryption:** Encrypting a password means converting it into a format that is unreadable without a specific decryption key.   
- **Hashing:** Hashing is more commonly used for passwords. It’s a one-way function that converts a password into a fixed-size string of characters, which cannot be easily reversed.   

**Common Methods:**   
**Hashing Algorithms:** MD5, SHA-256, bcrypt, Argon2.   
**Salting:** Adding random data (a salt) to the password before hashing it to ensure that even identical passwords result in different hashes.   

**Steps to Encrypt/Hash and Verify a Password:**   
**Hashing:** When a user sets a password, hash it using a secure algorithm.   
**Storing:** Store the hashed password (and salt, if used) in the database.   
**Verification:** When the user tries to log in, hash the input password and compare it to the stored hash.   

```python
import bcrypt

# Hash a password
hashed = bcrypt.hashpw(b'password123', bcrypt.gensalt())

# Check if an input password matches the hash
if bcrypt.checkpw(b'password123', hashed):
    print("Password is valid")
else:
    print("Invalid password")
```

# How to authenticate to a database using environment variables
## Why Use Environment Variables?
Environment variables allow you to store sensitive information like database credentials outside of your source code. This practice improves security by preventing sensitive data from being exposed in the codebase.   

### Steps to Authenticate Using Environment Variables:
- **Set Environment Variables:** Store the database username and password as environment variables.   
Linux or mac   
```
export DB_USERNAME='your_username'
```
Windows   
```
set DB_USERNAME=your_username
```
- **Access Variables in Code:** Use your programming language’s methods to access these variables.   
```
import os

db_username = os.getenv('DB_USERNAME')
```
- **Connect to the Database:** Use the retrieved credentials to authenticate and connect to the database.   
```
import psycopg2

conn = psycopg2.connect(
    dbname="mydatabase",
    user=db_username,
    password=db_password,
    host="localhost"
)
```