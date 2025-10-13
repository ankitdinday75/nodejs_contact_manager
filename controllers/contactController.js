const { randomUUID } = require('crypto');

const contacts = new Map();

const normalizeContact = (contact) => ({
  id: contact.id,
  name: contact.name,
  email: contact.email,
  phone: contact.phone,
});

const getContacts = (req, res) => {
  res.json({
    data: Array.from(contacts.values()).map(normalizeContact),
  });
};

const getContactById = (req, res) => {
  const contact = contacts.get(req.params.id);

  if (!contact) {
    return res.status(404).json({
      error: `Contact with id ${req.params.id} was not found`,
    });
  }

  return res.json({ data: normalizeContact(contact) });
};

const createContact = (req, res) => {
  const { name, email, phone } = req.body || {};

  if (!name || !email || !phone) {
    return res.status(400).json({
      error: 'name, email and phone are required to create a contact',
    });
  }

  const newContact = {
    id: randomUUID(),
    name,
    email,
    phone,
  };

  contacts.set(newContact.id, newContact);

  return res.status(201).json({ data: normalizeContact(newContact) });
};

const updateContact = (req, res) => {
  const existingContact = contacts.get(req.params.id);

  if (!existingContact) {
    return res.status(404).json({
      error: `Contact with id ${req.params.id} was not found`,
    });
  }

  const { name, email, phone } = req.body || {};

  if (!name && !email && !phone) {
    return res.status(400).json({
      error: 'At least one of name, email or phone must be provided to update a contact',
    });
  }

  const updatedContact = {
    ...existingContact,
    ...(name ? { name } : {}),
    ...(email ? { email } : {}),
    ...(phone ? { phone } : {}),
  };

  contacts.set(updatedContact.id, updatedContact);

  return res.json({ data: normalizeContact(updatedContact) });
};

const deleteContact = (req, res) => {
  if (!contacts.has(req.params.id)) {
    return res.status(404).json({
      error: `Contact with id ${req.params.id} was not found`,
    });
  }

  contacts.delete(req.params.id);

  return res.status(204).send();
};

module.exports = {
  getContacts,
  getContactById,
  createContact,
  updateContact,
  deleteContact,
};
