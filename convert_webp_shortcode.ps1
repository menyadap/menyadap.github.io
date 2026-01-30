# PowerShell script untuk mengubah {{< webp >}} shortcode ke Markdown image syntax

$blogDir = "src/content/blog"
$files = Get-ChildItem -Path $blogDir -Filter "*.md"

$stats = @{
    Converted = 0
    Unchanged = 0
    Errors = 0
}

Write-Host "Processing $($files.Count) markdown files...`n"

foreach ($file in $files | Sort-Object) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
        $originalContent = $content
        
        # Pattern untuk {{< webp src="..." caption="..." >}}
        $pattern = '\{\{<\s*webp\s+src="([^"]+)"\s+caption="([^"]+)"\s*>\}\}'
        
        # Replace dengan ![caption](src)
        $content = [regex]::Replace($content, $pattern, {
            param($match)
            $src = $match.Groups[1].Value
            $caption = $match.Groups[2].Value
            "![$caption]($src)"
        })
        
        if ($content -ne $originalContent) {
            Set-Content -Path $file.FullName -Value $content -Encoding UTF8
            Write-Host "[OK] $($file.Name) - WebP shortcode converted"
            $stats.Converted++
        } else {
            Write-Host "[--] $($file.Name) - No shortcode found"
            $stats.Unchanged++
        }
    }
    catch {
        Write-Host "[ERROR] $($file.Name) - $($_.Exception.Message)"
        $stats.Errors++
    }
}

Write-Host "`n$('='*60)"
Write-Host "Summary:"
Write-Host "  Converted: $($stats.Converted) files"
Write-Host "  Unchanged: $($stats.Unchanged) files"
Write-Host "  Errors: $($stats.Errors) files"
Write-Host "  Total: $($files.Count) files"
Write-Host "$('='*60)"
