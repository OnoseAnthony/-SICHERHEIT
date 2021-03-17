document.getElementById("open-popup-btn").addEventListener("click", function(){
    document.getElementsByClassName("popup")[0].classList.add("active");
  });

  document.getElementById("dismiss-popup-btn").addEventListener("click", function(){
    document.getElementsByClassName("popup")[0].classList.remove("active");
  });

  document.getElementById("open-show-password-popup-btn").addEventListener("click", function(){
    document.getElementsByClassName("show-password-popup")[0].classList.add("active");
  });

  document.getElementById("dismiss-show-password-popup-btn").addEventListener("click", function(){
    document.getElementsByClassName("show-password-popup")[0].classList.remove("active");
  });


  document.getElementById("open-delete-password-popup-btn").addEventListener("click", function(){
    document.getElementsByClassName("delete-password-popup")[0].classList.add("active");
  });

  document.getElementById("dismiss-delete-password-popup-btn").addEventListener("click", function(){
    document.getElementsByClassName("delete-password-popup")[0].classList.remove("active");
  });