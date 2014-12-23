function preloader() {
  if (document.images) {
      var img1 = new Image();
      var img2 = new Image();
      var img3 = new Image();
      var img4 = new Image();
      var img5 = new Image();
      var img6 = new Image();
      var img7 = new Image();
      var img8 = new Image();
      img1.src = "./pictures/hsa_hsa_Khan_Human_RNA_abundance_lv1.png";
      img2.src = "./pictures/hsa_hsa_Khan_Human_RNA_abundance_lv2.png";
      img3.src = "./pictures/hsa_hsa_Khan_Human_RNA_abundance_lv3.png";
      img4.src = "./pictures/hsa_hsa_Khan_Human_RNA_abundance_lv5.png";
      img5.src = "./pictures/hsa_hsa_Khan_Human_RNA_cost_lv1.png";
      img6.src = "./pictures/hsa_hsa_Khan_Human_RNA_cost_lv2.png";
      img7.src = "./pictures/hsa_hsa_Khan_Human_RNA_cost_lv3.png";
      img8.src = "./pictures/hsa_hsa_Khan_Human_RNA_cost_lv5.png";
  }
}
function addLoadEvent(func) {
  var oldonload = window.onload;
  if (typeof window.onload != 'function') {
    window.onload = func;
  } else {
    window.onload = function() {
      if (oldonload) {
        oldonload();
      }
      func();
    }
  }
}
addLoadEvent(preloader);
