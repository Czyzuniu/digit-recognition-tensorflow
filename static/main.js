window.addEventListener('load', () => {
  const canvas = new fabric.Canvas('canvas');
  canvas.isDrawingMode= true
  let width = 500, height = 500

  canvas.setHeight(height);
  canvas.setWidth(width);
  canvas.backgroundColor="black";

  let pencil = new fabric.PencilBrush(canvas)
  pencil.width = 80
  pencil.color = 'white'

  canvas.freeDrawingBrush = pencil

  const guessButton = window.guess

  guessButton.addEventListener('click', () => {
    exportCanvas(canvas).then((res) => {
      postData('/prediction', {base64:res.split("base64,")[1]}).then((response) => {
        alert(`I think its number ${response.prediction}`)
        canvas.clear();
        canvas.backgroundColor="black";
      })
    })
  })
})

function exportCanvas(canvas) {
  return new Promise((resolve) => {
    // let scaleRatio = Math.min(28/canvas.getWidth(), 28/canvas.getHeight());
    // canvas.setDimensions({ width: canvas.getWidth() * scaleRatio, height: canvas.getHeight() * scaleRatio })
    // canvas.setZoom(scaleRatio)
    const exportedImage = canvas.toDataURL({
      format: 'png',
    });

    resolve(exportedImage)
  })
}

function postData(url, data) {
  return new Promise((resolve, reject) => {
    fetch(url, {
      method: 'POST',
      headers: new Headers({'content-type': 'application/json'}),
      body: JSON.stringify(data),
    }).then(function (res) {
      return res.json()
    }).then((data) => {
      resolve(data)
    }).catch(error => {
      reject(error)
    });
  })
}
