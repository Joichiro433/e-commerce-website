<head>
  <link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/milligram/1.3.0/milligram.css" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css" />
</head>
<header id="header">
  <img src="ec_logo.svg" alt="Logo" />
  <input type="checkbox" class="menu-toggle" id="menu-toggle" />
  <nav class="header">
    <slot />
  </nav>
  <label for="menu-toggle" class="menu-nav-toggle">
    <span />
  </label>
</header>

<style>
  header {
    text-align: center;
    width: 100%;
    z-index: 999;
    position: fixed;
    background: #f4f5f6;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  header input.menu-toggle {
    display: none;
  }

  nav {
    position: absolute;
    text-align: center;
    top: 100%;
    left: 0;
    background-color: #f4f5f6;
    width: 100%;
    -webkit-transform: scale(1, 0);
    transform: scale(1, 0);
    -webkit-transition: -webkit-transform 400ms ease-in-out;
    transition: -webkit-transform 400ms ease-in-out;
    transition: transform 400ms ease-in-out;
    transition: transform 400ms ease-in-out, -webkit-transform 400ms ease-in-out;
    -webkit-transform-origin: top;
    transform-origin: top;
  }

  .menu-toggle:checked ~ nav {
    -webkit-transform: scale(1, 1);
    transform: scale(1, 1);
  }

  .menu-nav-toggle {
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    display: -webkit-box;
    display: -ms-flexbox;
    display: flex;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin-right: 2rem;
  }

  .menu-nav-toggle:hover,
  .menu-nav-toggle:focus {
    cursor: pointer;
  }

  .menu-nav-toggle span,
  .menu-nav-toggle span:before,
  .menu-nav-toggle span:after {
    display: block;
    background: #333;
    width: 2rem;
    border-radius: 0.125rem;
    position: relative;
    height: 0.25rem;
  }

  .menu-nav-toggle span:before,
  .menu-nav-toggle span:after {
    content: '';
    position: absolute;
  }

  .menu-nav-toggle span:before {
    top: 0.8rem;
  }

  .menu-nav-toggle span:after {
    bottom: 0.8rem;
  }

  @media screen and (min-width: 50rem) {
    .menu-nav-toggle {
      display: none;
    }
    header {
      display: -ms-grid;
      display: grid;
      -ms-grid-columns: 1fr auto minmax(37.5rem, 3fr) 1fr;
      grid-template-columns: 1fr auto minmax(37.5rem, 3fr) 1fr;
    }
    nav {
      all: unset;
      -ms-grid-column: 3;
      -ms-grid-column-span: 1;
      grid-column: 3/4;
      display: -webkit-box;
      display: -ms-flexbox;
      display: flex;
      -webkit-box-pack: end;
      -ms-flex-pack: end;
      justify-content: flex-end;
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
    }
  }
</style>
