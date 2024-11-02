

//cart plus
$(".plus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  console.log(id);
  
  var eml = this.parentNode.children[2];
  // console.log(id);
  $.ajax({
    type: "GET",
    url: "/pluscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      eml.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;
    },
  });
});

//cart minus
$(".minus-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var eml = this.parentNode.children[2];
  // console.log(id);
  $.ajax({
    type: "GET",
    url: "/minuscart",
    data: {
      prod_id: id,
    },
    success: function (data) {
      eml.innerText = data.quantity;
      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;
    },
  });
});

//Remove cart product
$(".remove-cart").click(function () {
  var id = $(this).attr("pid").toString();
  var eml = this;
  // console.log(id);
  $.ajax({
    type: "GET",
    url: "/removecart",
    data: {
      prod_id: id,
    },
    
    success: function (data) {

      if (data.amount === 0){
        console.log("hi")
        document.getElementById("image_show_em").style.display="block";
        document.querySelector(".off_cart").style.display="none";
        
      }

      document.getElementById("amount").innerText = data.amount;
      document.getElementById("totalamount").innerText = data.totalamount;
      eml.parentNode.parentNode.parentNode.parentNode.remove = "none";
      eml.parentNode.parentNode.parentNode.parentNode.remove();

      
    },
  });
});

//Remove cart product
$(".remove-address").click(function () {
  var id = $(this).attr("addressid").toString();
  var eml = this;
  console.log(id);
  $.ajax({
    type: "GET",
    url: "/remove-address",
    data: {
      prod_id: id,
    },
    success: function (data) {
      // Remove the address card from the DOM
      $(eml).closest(".col-sm-6").remove();

      // Check if no addresses remain
      if (data.status === "no_address") {
        document.getElementById("profile-block-address").style.display = "block";
      }
    },
  });
});
