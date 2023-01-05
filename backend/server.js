const express = require("express");
const morgan = require("morgan");
const cors = require("cors");
const helmet = require("helmet");
const expressJSDocSwagger = require("express-jsdoc-swagger");
const { ethers } = require("ethers");
require("dotenv").config();

const cron = require("node-cron");

const connectDB = require("./config/db");

// ----------------------------------
// JSDOC Settings
// ----------------------------------

const jsdocOptions = {
  info: {
    version: "1.0.0",
    title: "Argonauts API",
    description:
      "Argonauts API Documentation, production server: https://argonauts-nft.herokuapp.com/",
    license: {
      name: "MIT",
    },
  },
  security: {
    BasicAuth: {
      type: "http",
      scheme: "basic",
    },
  },
  baseDir: __dirname,
  // Glob pattern to find your jsdoc files (multiple patterns can be added in an array)
  filesPattern: "./**/*.js",
  // URL where SwaggerUI will be rendered
  swaggerUIPath: "/api-docs",
  // Expose OpenAPI UI
  exposeSwaggerUI: true,
  // Expose Open API JSON Docs documentation in `apiDocsPath` path.
  exposeApiDocs: false,
  // Open API JSON Docs endpoint.
  apiDocsPath: "/v3/api-docs",
  // Set non-required fields as nullable by default
  notRequiredAsNullable: false,
  // You can customize your UI options.
  // you can extend swagger-ui-express config. You can checkout an example of this
  // in the `example/configuration/swaggerOptions.js`
  swaggerUiOptions: {},
  // multiple option in case you want more that one instance
  multiple: true,
};

// ----------------------------------
// Routes Import
// ----------------------------------

const account = require("./routes/Account");

// ----------------------------------
// Middleware
// ----------------------------------
const app = express();

// app.use(cors());
// app.use(helmet());

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

if (process.env.NODE_ENV === "dev") {
  app.use(morgan("dev"));
}
expressJSDocSwagger(app)(jsdocOptions);

// ----------------------------------
// API Routes
// ----------------------------------

app.use("/account", account);

app.get("/", (req, res) => {
  res.status(301).redirect("/api-docs");
});
// ----------------------------------
// Express server
// ----------------------------------
const PORT = process.env.PORT || 4000;
// app.db = connectDB();

app.server = app.listen(PORT, () => {
  console.log(`Server started on port ${PORT}`);
});

module.exports = app;
