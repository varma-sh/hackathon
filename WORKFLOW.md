# AI Research Paper Writer - Workflow Diagram

```
┌─────────────────┐
│   User Input    │
│                 │
│ • Topic         │
│ • Format        │
│ • Length        │
│ • Output Type   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│   Validation    │
│                 │
│ • Check inputs  │
│ • Validate      │
│   format        │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐     ┌─────────────────┐
│   API Call      │────▶│   Mock Response │
│   (Optional)    │     │   (Current)     │
│                 │     │                 │
│ • Groq API      │     │ • Sample Paper  │
│ • Generate      │     │ • Dynamic       │
│   Paper         │     │   Content       │
└─────────┬───────┘     └─────────┬───────┘
          │                       │
          └───────────────────────┘
                    │
                    ▼
          ┌─────────────────┐
          │   Display       │
          │   Result        │
          │                 │
          │ • Show Paper    │
          │ • Download Btn  │
          └─────────┬───────┘
                    │
                    ▼
          ┌─────────────────┐
          │   Download      │
          │   (Optional)    │
          │                 │
          │ • .txt File     │
          │ • Browser       │
          │   Download      │
          └─────────────────┘
```

## Workflow Steps:

1. **User Input**: User fills the form with topic, format, length, and output type
2. **Validation**: Backend validates all inputs for correctness
3. **Generation**: Either calls Groq API (when valid key) or uses mock response
4. **Display**: Shows the generated paper in the result section
5. **Download**: User can optionally download the paper as a .txt file

## Key Components:

- **Frontend**: HTML form with JavaScript for interaction
- **Backend**: Flask app handling requests and responses
- **API**: Groq API for AI-generated content (currently mocked)
- **Download**: Client-side JavaScript for file download

## Data Flow:

Form Data → Flask Route → Validation → Generation → JSON Response → Frontend Display → Optional Download
