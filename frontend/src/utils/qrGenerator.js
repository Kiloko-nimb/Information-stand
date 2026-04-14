import QRCode from 'qrcode'

export async function generateQRCode(url) {
  try {
    const qrDataUrl = await QRCode.toDataURL(url, {
      width: 200,
      margin: 1,
      color: {
        dark: '#2c3e50',
        light: '#ffffff'
      }
    })
    return qrDataUrl
  } catch (error) {
    console.error('Ошибка генерации QR-кода:', error)
    return null
  }
}
