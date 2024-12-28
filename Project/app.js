const express = require('express');
const mysql = require('mysql2');
const bodyParser = require('body-parser');
const session = require('express-session');

const app = express();
const port = 3001;

// Create MySQL connection
const con = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'raz12345',
  database: 'speedx2'
});

// Connect to MySQL
con.connect((err) => {
  if (err) {
    console.error('Error connecting to database:', err);
    return;
  }
  console.log('Connected to MySQL database');
});

// Middleware to parse request body
app.use(bodyParser.urlencoded({ extended: true }));

// Serve static files (including login.html)
app.use(express.static('public'));

// Session middleware
app.use(session({
  secret: 'secret_key', // Change this to a secure random string
  resave: false,
  saveUninitialized: true
}));

// Define route for the login page
app.get('/', (req, res) => {
  res.sendFile(__dirname + '/login.html');
});

// Define login route
app.post('/login', (req, res) => {
  const username = req.body.username;
  const password = req.body.password;

  // Query the database to check if username and password match
  con.query('SELECT * FROM customer WHERE customer_name = ? AND customer_password = ?', [username, password], (err, results) => {
    if (err) {
      console.error('Error executing query:', err);
      res.status(500).send('Internal Server Error');
      return;
    }
    
    // If user found
    if (results.length > 0) {
      const user = results[0];
      
      // Check user's role
      if (user.user_role === 2) {
        // If user is admin, redirect to inventory analysis
        req.session.user = user; // Store user information in session
        res.sendFile(__dirname + '/inventory.html');
      } else if (user.user_role === 1) {
        // If user is user, redirect to homepage.html
        req.session.user = user; // Store user information in session
        res.sendFile(__dirname + '/homepage.html');
      } else {
        // For other roles, redirect back to login page
        res.redirect('/');
      }
    } else {
      // If user not found, redirect back to login page
      res.redirect('/');
    }
  });
});

// Define route for the registration page
app.get('/register', (req, res) => {
  res.sendFile(__dirname + '/register.html');
});

// Define registration route
app.post('/register', (req, res) => {
  const { username, password, contact_number, address, email, pincode } = req.body;

  // Query to get the highest existing customer_ID
  con.query('SELECT MAX(customer_ID) AS max_customer_id FROM customer', (err, result) => {
    if (err) {
      console.error('Error fetching max customer ID:', err);
      res.status(500).send('Internal Server Error');
      return;
    }

    // Calculate the next available customer_ID
    const nextCustomerId = result[0].max_customer_id ? result[0].max_customer_id + 1 : 1;

    // Insert new customer into the database with the next available customer_ID and default user_role value
    con.query('INSERT INTO customer (customer_ID, customer_name, customer_password, contact_number, customer_address, customer_email_id, customer_pincode, user_role) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', [nextCustomerId, username, password, contact_number, address, email, pincode, 1], (err, result) => {
      if (err) {
        console.error('Error registering new customer:', err);
        res.status(500).send('Internal Server Error');
        return;
      }
      console.log('New customer registered successfully');
      // Redirect to login page after registration
      res.redirect('/');
    });
  });
});

// Homepage - Retrieve product listing
app.get('/products', (req, res) => {
  con.query('SELECT * FROM product', (err, results) => {
      if (err) {
          console.error('Error fetching product listing:', err);
          res.status(500).send('Internal Server Error');
          return;
      }
      res.json(results);
  });
});

// Define route to fetch product inventory with sorting for inventory html
app.get('/product-inventory', (req, res) => {
  const sortColumn = req.query.sortColumn || 'product_ID';
  const sortOrder = req.query.sortOrder || 'asc';

  con.query(`
    SELECT p.product_ID, p.product_name, c.category_name, p.product_price, SUM(si.quantity) AS total_stock
    FROM product p
    LEFT JOIN store_inventory si ON p.product_ID = si.product_ID
    JOIN category c ON p.category_ID = c.category_ID
    GROUP BY p.product_ID
    ORDER BY ${sortColumn} ${sortOrder}
  `, (err, results) => {
    if (err) {
      console.error('Error fetching product inventory:', err);
      res.status(500).json({ error: 'Internal Server Error' });
      return;
    }
    res.json(results);
  });
});

// Define route for ordering page
app.get('/ordering', (req, res) => {
  if (!req.session.user) {
    res.redirect('/');
    return;
  }
  res.sendFile(__dirname + '/ordering.html');
});

// Define route for cart page
app.get('/cart', (req, res) => {
  if (!req.session.user) {
    res.redirect('/');
    return;
  }

  const customerId = req.session.user.customer_ID;
  // Query the database to fetch cart items for the logged-in customer
  con.query('SELECT * FROM cart WHERE customer_ID = ?', [customerId], (err, results) => {
    if (err) {
      console.error('Error fetching cart items:', err);
      res.status(500).send('Internal Server Error');
      return;
    }
    // Render the cart page with cart items
    res.render('cart', { cartItems: results });
  });
});

// Define route to add product to cart
app.post('/add-to-cart', (req, res) => {
  if (!req.session.user) {
    res.status(401).send('Unauthorized');
    return;
  }

  const productId = req.body.productId;
  const quantity = req.body.quantity;
  const customerId = req.session.user.customer_ID;

  // Insert product into cart table with customer ID
  con.query('INSERT INTO cart (customer_ID, product_ID, quantity) VALUES (?, ?, ?)', [customerId, productId, quantity], (err, result) => {
    if (err) {
      console.error('Error adding product to cart:', err);
      res.status(500).send('Internal Server Error');
      return;
    }
    console.log('Product added to cart successfully');
    res.status(200).send('Product added to cart successfully');
  });
});

// Start server
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
