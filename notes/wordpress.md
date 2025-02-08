# WordPress

## Table of Contents

- [WordPress](#wordpress)
  - [Table of Contents](#table-of-contents)
  - [Documentation](#documentation)
  - [Common WordPress Errors](#common-wordpress-errors)
  - [Debugging Steps](#debugging-steps)
  - [Debugging Tools](#debugging-tools)

## Documentation

- [wp-cli](https://developer.wordpress.org/cli/commands/)
- [Documentation Overview](https://www.wordpress.info/doc/overview/)
- [Tutorials](https://wordpress.com/learn/)

## Common WordPress Errors

1. **HTTP Errors**

- **404 Not Found**: Page or resource missing.
- **403 Forbidden**: Insufficient permissions to access the resource.
- **500 Internal Server Error**: Generic error, often caused by server misconfiguration or PHP errors.
- **503 Service Unavailable**: Server is overloaded or in maintenance mode.

2. **Database Errors**

- **Error Establishing a Database Connection**: Database credentials incorrect or database server is down.
- **Table Prefix Issues**: Wrong `$table_prefix` in `wp-config.php`.
- **Corrupt Database**: Can be fixed using `wp db repair`.

3. **PHP Errors**

- **Parse Error**: Syntax error in PHP files.
- **Fatal Error**: Missing function or class.
- **Deprecated Function Warnings**: Old functions being used.

## Debugging Steps

1. **Enable Debug Mode**

Edit `wp-config.php`:

```php
// Enable Debug Mode
define('WP_DEBUG', true);
// Enable Debug logging to the /wp-content/debug.log file
define('WP_DEBUG_LOG', true);
// Disable display of WordPress errors and warnings
define('WP_DEBUG_DISPLAY', false);
// Disable display of PHP errors and warnings
@ini_set('display_errors', 0);
```

Logs will be saved in `wp-content/debug.log`.

2. **Check `.htaccess`**

Ensure WordPress rules exist:

```apache
# BEGIN WordPress

<IfModule mod_rewrite.c>
RewriteEngine On
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
RewriteBase /
RewriteRule ^index\.php$ - [L]
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule . /index.php [L]
</IfModule>

# END WordPress
```

3. **Check Apache and VirtualHost config**

**Redhat and derivatives**

- `/etc/httpd/conf/httpd.conf`
- `/etc/httpd/conf.d/welcome.conf`

**Debian and derivatives**

- `/etc/apache2/apache2.conf`
- `/etc/apache2/sites-available/000-default.conf`

```apache
<Directory "/var/www">
    AllowOverride All
    # Allow open access:
    Require all granted
</Directory>
<Directory "/var/www/html">
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>
```

4. **Reset File Permissions**

```bash
find /var/www/html -type d -exec chmod 755 {} \;
find /var/www/html -type f -exec chmod 644 {} \;
```

4. **Disable Plugins & Themes**

Hide the plugin directory:

```bash
mv wp-content/plugins wp-content/.plugins
```

Switch to a default theme:

```bash
wp theme install twentytwentyfive --activate
wp theme activate twentytwentyfive
```

5. **Check Server Logs**

For Apache:

```bash
tail -f /var/log/httpd/error_log
```

For Nginx:

```bash
tail -f /var/log/nginx/error.log
```

6. **Verify Database Connection**

```bash
wp db check
```

If corrupt:

```bash
wp db repair
```

7. **Increase Memory Limit**

Edit `wp-config.php`:

```php
define('WP_MEMORY_LIMIT', '256M');
```

## Debugging Tools

- **WP-CLI**: Command-line interface for WordPress.
- **Query Monitor**: Plugin for analyzing database queries and errors.
- **Health Check & Troubleshooting**: Plugin for diagnosing issues.
