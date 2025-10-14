# Invoice Tracker - Frontend-Backend Integration Guide

## Overview
The tracker.html frontend is now fully connected to the FastAPI backend with complete CRUD (Create, Read, Update, Delete) functionality for invoices stored in MySQL database.

## Changes Made

### Backend (main.py)

1. **CORS Middleware Added**
   - Allows frontend to make API requests from any origin
   - In production, update `allow_origins` to specific domains

2. **New API Endpoints**
   - `PUT /invoices/{invoice_id}` - Update an existing invoice
   - `DELETE /invoices/{invoice_id}` - Delete an invoice
   - `GET /` - Serves the tracker.html page

3. **Pydantic Model**
   - `InvoiceUpdate` model for validating invoice update requests

4. **Database Operations**
   - Updates and deletes are synced to both MySQL and Excel file

### Frontend (tracker.html)

1. **API Integration**
   - `fetchInvoices()` - Fetches all invoices from backend on dashboard load
   - `updateInvoiceAPI()` - Updates invoice via PUT request
   - `deleteInvoiceAPI()` - Deletes invoice via DELETE request

2. **Data Transformation**
   - Backend data is transformed to match frontend format
   - Handles missing fields (service, phone_number) gracefully

3. **Async Operations**
   - All CRUD operations are now asynchronous
   - Proper error handling with user feedback

## How to Use

### Starting the Application

1. **Start the FastAPI Backend**
   ```bash
   cd /home/dhurkesh/Documents/GitHub/invoice-project
   uvicorn main:app --reload
   ```

2. **Access the Application**
   - Open browser and navigate to: `http://localhost:8000`
   - Or open `tracker.html` directly in browser (API calls will work via CORS)

### Login Credentials
- **Email**: bharad008@rmkcet.ac.in
- **Password**: 123

### Features

1. **View Invoices**
   - All invoices from MySQL database are displayed
   - Real-time statistics (Total, Paid, Unpaid)
   - Search and sort functionality

2. **Edit Invoice**
   - Click "Edit" button on any invoice
   - Modify fields and save
   - Changes are saved to MySQL and Excel

3. **Delete Invoice**
   - Click "Delete" button on any invoice
   - Confirm deletion in modal
   - Invoice is removed from MySQL and Excel

4. **Add Invoice**
   - Click "Add New Invoice" button
   - Fill in details
   - Note: Manual additions are local only (use OCR upload for backend storage)

## API Endpoints

### GET /invoices/
Retrieves all invoices from database
```json
{
  "count": 2,
  "invoices": [
    {
      "id": 1,
      "client_name": "ABC Corp",
      "invoice_number": "INV001",
      "invoice_date": "2025-10-13",
      "due_date": "2025-10-21",
      "subtotal": 9000.00,
      "tax": 1000.00,
      "total": 10000.00,
      "status": "Paid"
    }
  ]
}
```

### PUT /invoices/{invoice_id}
Updates an existing invoice
```json
{
  "client_name": "ABC Corp",
  "invoice_number": "INV001",
  "invoice_date": "2025-10-13",
  "due_date": "2025-10-21",
  "subtotal": 9000.00,
  "tax": 1000.00,
  "total": 10000.00,
  "status": "Paid"
}
```

### DELETE /invoices/{invoice_id}
Deletes an invoice by ID
```json
{
  "message": "Invoice deleted successfully",
  "id": 1
}
```

## Database Schema

The MySQL `invoices` table contains:
- `id` - Auto-increment primary key
- `client_name` - Client name
- `invoice_number` - Unique invoice number
- `invoice_date` - Invoice date
- `due_date` - Payment due date
- `subtotal` - Amount before tax
- `tax` - Tax amount
- `total` - Total amount (subtotal + tax)
- `status` - Payment status (Paid/Unpaid)

## Notes

- The frontend displays `total` as `amount` for consistency
- Service and phone_number fields are frontend-only (not in backend schema)
- Manual invoice additions are local only; use OCR upload endpoint for backend persistence
- All dates are in YYYY-MM-DD format

## Troubleshooting

1. **CORS Errors**: Ensure FastAPI server is running and CORS is enabled
2. **Connection Refused**: Check if backend is running on port 8000
3. **Database Errors**: Verify MySQL connection settings in main.py
4. **No Invoices Displayed**: Check browser console for API errors
