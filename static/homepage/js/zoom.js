 img[data-action="zoom"] {
    cursor: pointer;
    cursor: -webkit-zoom-in;
    cursor: -moz-zoom-in;
  }
  .zoom-img,
  .zoom-img-wrap {
    position: relative;
    z-index: 666;
    -webkit-transition: all 300ms;
         -o-transition: all 300ms;
            transition: all 300ms;
  }
  img.zoom-img {
    cursor: pointer;
    cursor: -webkit-zoom-out;
    cursor: -moz-zoom-out;
  }
  .zoom-overlay {
    z-index: 420;
    background: #fff;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    pointer-events: none;
    filter: "alpha(opacity=0)";
    opacity: 0;
    -webkit-transition:      opacity 300ms;
         -o-transition:      opacity 300ms;
            transition:      opacity 300ms;
  }
  .zoom-overlay-open .zoom-overlay {
    filter: "alpha(opacity=100)";
    opacity: 1;
  }
  .zoom-overlay-open,
  .zoom-overlay-transitioning {
    cursor: default;
  }