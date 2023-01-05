const express = require("express");
const router = express.Router();

const {
  getBalance,
  getDepositAddress,
  withdraw,
  create,
} = require("../controllers/Account");

router.route("/getBalance").get(getBalance);
router.route("/getDepositAddress").get(getDepositAddress);
router.route("/create").post(create);
router.route("/withdraw").post(withdraw);

module.exports = router;
