const express = require('express');
const router = express.Router();
const dotenv = require('dotenv').config();
// const { body, validationResult } = require('express-validator');
const { getContacts, createContact, updateContact, getContact, deleteContact } = require('../Controllers/contactController');
// const { getContacts, createContact, updateContact, deleteContact } = require('../controllers/contactController');
// const { protect } = require('../middleware/authMiddleware');
// // Routes
// router.route('/').get(protect, getContacts).post(protect, createContact);

// router.route('/:id').put(protect, updateContact).delete(protect, deleteContact);

// router.route('/').get((req, res) => {
//     res.status(200).json({message:'Get all contacts'});
// }).post((req, res) => {
//     res.status(201).json({message:'Create a contact'});
// });

router.route('/').get(getContacts).post(createContact);

router.route('/:id').put(updateContact).get(getContact).delete(deleteContact);

module.exports = router;