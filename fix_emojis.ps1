$files = Get-ChildItem -Path "src/content/blog/*.md" -File
$fixed = 0
$total = $files.Count

Write-Host "Processing $total files to fix emoji encoding..."

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $original = $content
    
    # Replace corrupted emojis with correct ones
    $content = $content -replace 'ðŸ"±', '📱'
    $content = $content -replace 'ðŸ'¬', '💬'
    $content = $content -replace 'ðŸ"·', '📷'  
    $content = $content -replace 'ðŸ"ž', '📞'
    $content = $content -replace 'ðŸ"'', '🔒'
    $content = $content -replace 'ðŸ˜‹', '😋'
    $content = $content -replace 'ðŸ'‡', '👇'
    $content = $content -replace 'ðŸ'‰', '👉'
    
    if ($content -ne $original) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
        $fixed++
    }
}

Write-Host "Fixed $fixed files out of $total"
