---
description: Test MiMo API connection with a given key. Calls the MiMo API endpoint and returns the response.
---
# MiMo API Test

Test MiMo API connectivity with a specific API key.

## Usage
Run this command with an API key to verify it works:
```
/test-mimo-api <api_key>
```

## Implementation

1. Determine endpoint based on key prefix:
   - `sk-` keys → `https://api.xiaomimimo.com/v1`
   - `tp-` keys → `https://token-plan-cn.xiaomimimo.com/v1`

2. Make a simple test call using PowerShell:
```powershell
$headers = @{
    "Authorization" = "Bearer $ARGUMENTS"
    "Content-Type" = "application/json"
}
$body = @{
    model = "mimo-v2.5-pro"
    messages = @(@{ role = "user"; content = "Say hello in one word" })
    max_tokens = 50
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://api.xiaomimimo.com/v1/chat/completions" -Method Post -Headers $headers -Body $body
```

3. Report:
   - Key prefix (sk-/tp-)
   - Endpoint used
   - Response status
   - Model used
   - Token count (if available)
   - Error message (if failed)

## Known Issues
- Token Plan keys (`tp-`) may return "Invalid API Key" if not activated
- Old keys may return 402 "Insufficient account balance"
- PowerShell `curl` syntax differs from bash — use `Invoke-RestMethod`
