  window.onload = function() {
    placeSearch({
      key: 'n2BFbDxJHnrRNG5um6e81nYoGcHGbBm7',
      container: document.querySelector('#search-input'),
      useDeviceLocation: true,
      collection: [
        'poi',
        'address',
        'adminArea',
      ]
    });
  }

