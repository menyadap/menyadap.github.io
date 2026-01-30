# PowerShell script to convert HTML card to Markdown blockquote

$blogDir = "src/content/blog"
$files = Get-ChildItem -Path $blogDir -Filter "*.md" | Sort-Object

$converted = 0
$unchanged = 0  
$errors = 0

Write-Host "Processing $($files.Count) markdown files...`n"

# Read the replacement content from file
$newContent = Get-Content -Path "replacement_content.txt" -Raw -Encoding UTF8

# Pattern untuk old HTML card structure
$pattern = '<div class="d-flex justify-content-center">.*?</div>\s*</div>\s*$'

foreach ($file in $files) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
        
        if ($content -match 'd-flex justify-content-center') {
            # Replace using regex
            $result = [regex]::Replace($content, $pattern, $newContent, [System.Text.RegularExpressions.RegexOptions]::Singleline -bor [System.Text.RegularExpressions.RegexOptions]::Multiline)
            
            if ($result -ne $content) {
                Set-Content -Path $file.FullName -Value $result -Encoding UTF8
                Write-Host "[OK] $($file.Name) - Converted"
                $converted++
            }
            else {
                Write-Host "[--] $($file.Name) - Card found but not replaced"
                $unchanged++
            }
        }
        else {
            Write-Host "[--] $($file.Name) - No card found"
            $unchanged++
        }
    }
    catch {
        Write-Host "[ERROR] $($file.Name) - $($_.Exception.Message)"
        $errors++
    }
}

Write-Host ""
Write-Host "============================================================"
Write-Host "Summary:"
Write-Host "  Converted: $converted files"
Write-Host "  Unchanged: $unchanged files"
Write-Host "  Errors: $errors files"
Write-Host "  Total: $($files.Count) files"
Write-Host "============================================================"
