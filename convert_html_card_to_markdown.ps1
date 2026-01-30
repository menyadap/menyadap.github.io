# PowerShell script untuk mengubah HTML card menjadi Markdown blockquote

$blogDir = "src/content/blog"
$files = Get-ChildItem -Path $blogDir -Filter "*.md"

$stats = @{
    Converted = 0
    Unchanged = 0
    Errors = 0
}

Write-Host "Processing $($files.Count) markdown files...`n"

# New Markdown blockquote format
$newContent = @"
> ## ADA **PERTANYAAN**?
>
> ![Layanan Monitoring Perangkat](/images/monitoring-device.webp)
>
> 📱 **Mendukung iPhone & Android**
>
> 💬 Monitoring aktivitas aplikasi pesan  
> (WhatsApp, Telegram, Line, Instagram, Facebook, Skype, Viber, Snapchat)
>
> 📷 Pemantauan layar & kamera **dengan izin pemilik perangkat**
>
> 📞 Riwayat panggilan telepon & akses galeri
>
> 🔒 **Ketentuan penggunaan & privasi berlaku**  
> Layanan ini hanya untuk **pengawasan sah**, seperti:
> - kontrol orang tua
> - monitoring perangkat pribadi
> - pengelolaan perangkat kerja
>
> 😋 **Masih ada pertanyaan?**  
> Tinggal klik aja 👇
>
> 👉 **Chat WhatsApp:**  
> https://wa.me/628128398998288
"@

foreach ($file in $files | Sort-Object) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
        $originalContent = $content
        
        # Check if file contains the HTML card pattern
        if ($content -match 'd-flex justify-content-center') {
            # Find and replace the HTML card structure with Markdown
            # Pattern: from <div class="d-flex...  to </div></div>
            $pattern = '<div class="d-flex justify-content-center">\s*<div class="col-lg-6">\s*<div class="card row related mb-5 mt-5">\s*<div class="card-body">.*?</div>\s*</div>\s*</div>\s*</div>'
            
            if ([regex]::IsMatch($content, $pattern, [System.Text.RegularExpressions.RegexOptions]::Singleline)) {
                $content = [regex]::Replace($content, $pattern, $newContent, [System.Text.RegularExpressions.RegexOptions]::Singleline)
                Set-Content -Path $file.FullName -Value $content -Encoding UTF8
                Write-Host "[OK] $($file.Name) - HTML card converted"
                $stats.Converted++
            } else {
                Write-Host "[--] $($file.Name) - Card pattern found but not matched exactly"
                $stats.Unchanged++
            }
        } else {
            Write-Host "[--] $($file.Name) - No card found"
            $stats.Unchanged++
        }
    }
    catch {
        Write-Host "[ERROR] $($file.Name) - $($_.Exception.Message)"
        $stats.Errors++

Write-Host "`n$('='*60)"
Write-Host "Summary:"
Write-Host "  Converted: $($stats.Converted) files"
Write-Host "  Unchanged: $($stats.Unchanged) files"
Write-Host "  Errors: $($stats.Errors) files"
Write-Host "  Total: $($files.Count) files"
Write-Host "$('='*60)"
