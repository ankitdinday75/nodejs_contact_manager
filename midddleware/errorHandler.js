const { constants } = require("../constants");

const errorHandler = (err, req, res, next) => {
    const statusCode = res.statusCode ? res.statusCode : 500;

    switch (statusCode) {
        case constants.Validation_Error:
            res.json({
                Title: 'Validation Failed',
                message: err.message,
                stack: err.stack,
            });
    case constants.Not_Found:
        res.json({
            Title: 'Not Found',
            message: err.message,
            stack: err.stack,
        });
        case constants.Server_Error:
        res.json({
            Title: 'server error',
            message: err.message,
            stack: err.stack,
        });
        case constants.Forbidden:
        res.json({
            Title: 'Forbidden',
            message: err.message,
            stack: err.stack,
        });
        default:
        console.log('No Error, All Good');
            break;
    }

    res.status(statusCode);
  
}

module.exports = { errorHandler };