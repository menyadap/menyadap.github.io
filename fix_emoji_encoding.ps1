# Fix encoding issue in markdown files - replace corrupted emojis

$blogDir = "src/content/blog"
$files = Get-ChildItem -Path $blogDir -Filter "*.md" | Sort-Object

$fixed = 0
$checked = 0

Write-Host "Checking and fixing corrupted emojis...`n"

# Mapping corrupted emoji to correct ones
$emojiMap = @{
    'ðŸ"±' = '📱'
    'ðŸ'¬' = '💬'
    'ðŸ"·' = '📷'
    'ðŸ"ž' = '📞'
    'ðŸ"'' = '🔒'
    'ðŸ˜‹' = '😋'
    'ðŸ'‡' = '👇'
    'ðŸ'‰' = '👉'
}

foreach ($file in $files) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
        $originalContent = $content
        
        # Check and replace corrupted emojis
        $hasCorrupted = $false
        foreach ($corrupted in $emojiMap.Keys) {
            if ($content -match [regex]::Escape($corrupted)) {
                $hasCorrupted = $true
                $correct = $emojiMap[$corrupted]
                $content = $content -replace [regex]::Escape($corrupted), $correct
            }
        }
        
        if ($hasCorrupted) {
            Set-Content -Path $file.FullName -Value $content -Encoding UTF8
            Write-Host "[FIXED] $($file.Name)"
            $fixed++
        }
        
        $checked++
    }
    catch {
        Write-Host "[ERROR] $($file.Name) - $($_.Exception.Message)"
    }
}

Write-Host "`n============================================================"
Write-Host "Summary:"
Write-Host "  Checked: $checked files"
Write-Host "  Fixed: $fixed files"
Write-Host "============================================================"
