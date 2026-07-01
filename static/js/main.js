// CardioPredict - shared front-end behaviour

document.addEventListener('DOMContentLoaded', function () {
  // Auto-dismiss alert banners after a few seconds.
  document.querySelectorAll('.alert').forEach(function (alertEl) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
      if (bsAlert) bsAlert.close();
    }, 5000);
  });
});
