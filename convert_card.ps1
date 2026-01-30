# PowerShell script to convert HTML card to Markdown blockquote

$blogDir = "src/content/blog"
$files = Get-ChildItem -Path $blogDir -Filter "*.md" | Sort-Object

$converted = 0
$unchanged = 0
$errors = 0

Write-Host "Processing $($files.Count) markdown files...`n"

$newContent = '> ## ADA **PERTANYAAN**?
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
> https://wa.me/628128398998288'

$pattern = '<div class="d-flex justify-content-center">.*?</div>\s*</div>'

foreach ($file in $files) {
    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
        $originalContent = $content
        
        if ($content -match 'd-flex justify-content-center') {
            $newContent_escaped = [regex]::Escape($newContent)
            $result = [regex]::Replace($content, $pattern, $newContent, [System.Text.RegularExpressions.RegexOptions]::Singleline)
            
            if ($result -ne $originalContent) {
                Set-Content -Path $file.FullName -Value $result -Encoding UTF8
                Write-Host "[OK] $($file.Name) - Card converted"
                $converted++
            }
            else {
                Write-Host "[--] $($file.Name) - Card found but replacement failed"
                $unchanged++
            }
        }
        else {
            Write-Host "[--] $($file.Name) - No card"
            $unchanged++
        }
    }
    catch {
        Write-Host "[ERROR] $($file.Name)"
        $errors++
    }
}

Write-Host "`n============================================================"
Write-Host "Summary:"
Write-Host "  Converted: $converted files"
Write-Host "  Unchanged: $unchanged files"
Write-Host "  Errors: $errors files"
Write-Host "  Total: $($files.Count) files"
Write-Host "============================================================"
