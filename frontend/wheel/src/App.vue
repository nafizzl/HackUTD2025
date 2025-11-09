<template>
  <div id="app-container">
    <router-view />
  </div>
</template>

<style>
/* Global styles for your app */
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  margin: 0;
  background-color: #f4f4f4;
  color: #333;
}

#app-container {
  max-width: 500px;
  margin: 0 auto;
  background-color: #fff;
  min-height: 100vh;
  box-shadow: 0 0 20px rgba(0,0,0,0.05);
}
</style>