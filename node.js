const puppeteer = require('puppeteer');
const fs = require('fs');

async function spamReport(phoneNumber, count) {
    console.log(`Memulai spam ke ${phoneNumber}...`);
    
    // Buka browser
    const browser = await puppeteer.launch({ headless: false }); // Set headless: false untuk melihat prosesnya
    const page = await browser.newPage();
    
    // Buka WhatsApp Web
    await page.goto('https://web.whatsapp.com');
    console.log('Silakan scan QR Code...');
    
    // Tunggu sampai login selesai
    await page.waitForNavigation({ waitUntil: 'networkidle0' });
    
    for (let i = 0; i < count; i++) {
        try {
            // Cari kolom pencarian
            await page.click('div[contenteditable="true"][data-tab="3"]');
            await page.keyboard.type(phoneNumber);
            await page.keyboard.press('Enter');
            
            // Tunggu chat terbuka
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Klik menu tiga titik
            await page.click('div[title="Three dots"]');
            await page.click('div[role="menuitem"]:nth-child(4)'); // Asumsi ini menu Report
            
            // Konfirmasi report
            await page.click('button[type="submit"]');
            
            console.log(`Laporan ${i + 1}/${count} terkirim.`);
            
            // Kembali ke beranda
            await page.click('div[title="Menu"]');
        } catch (error) {
            console.error(`Gagal pada laporan ${i + 1}:`, error.message);
        }
        
        // Jeda agar terlihat seperti manusia
        await new Promise(resolve => setTimeout(resolve, Math.random() * 5000 + 2000));
    }
    
    await browser.close();
    console.log('Selesai!');
}

// Jalankan fungsi
spamReport('628xxxxxxxxxx', 50);
