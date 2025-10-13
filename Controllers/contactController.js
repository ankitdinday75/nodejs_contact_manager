
const asyncHandler = require('express-async-handler');

const getContacts = asyncHandler(async (req, res) => {
    res.status(200).json({
        message: 'get all contacts'
    });
})

const createContact = asyncHandler(async (req, res) => {

    const { name, email, phone } = req.body;
    if (!name || !email || !phone) {
        res.status(400);
        throw new Error('All fields are mandatory!');
    }
    res.status(201).json({
        message: 'Create contact'
    });
})

const updateContact = asyncHandler(async (req, res) => {
    res.status(200).json({
        message: `update the contact ${req.params.id}`
    });
})

const getContact = asyncHandler(async (req, res) => {
    res.status(200).json({
        message: 'get contact for id ' + req.params.id
    });
})

const deleteContact = asyncHandler(async (req, res) => {
    res.status(200).json({
        message: 'delete contact for id ' + req.params.id
    });
})

module.exports = { getContacts, createContact, updateContact, getContact, deleteContact };