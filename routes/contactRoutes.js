const express = require('express');
const router = express.Router();
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

router.route('/').get((req, res) => {
    res.status(200).json({
        message: 'get all contacts'
    });
})

router.route('/').post((req, res) => {
    res.status(200).json({
        message: 'Create contact'
    });
})

router.route('/:id').put((req, res) => {
    res.status(200).json({
        message: `get all contacts ${req.params.id}`
    });
})

router.route('/:id').get((req, res) => {
    res.status(200).json({
        message: 'get contact for id ' + req.params.id
    });
})

router.route('/:id').delete((req, res) => {
    res.status(200).json({
        message: 'delete contact for id ' + req.params.id
    });
})

module.exports = router;