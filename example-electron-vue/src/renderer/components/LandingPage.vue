<template>
  <div id="wrapper">
      <div class="id-card-wrapper">
          <div class="id-card">
              <div class="profile-row">
                  <span v-show="inserted" style="position: absolute;color: chartreuse;font-weight: bold;">card inserted</span>
                  <span v-show="removed" style="position: absolute;color: red;font-weight: bold;">card removed</span>
                  <div class="dp">
                      <img :src="base64photo">
                  </div>
                  <div class="desc">
                      <h1>{{name}}</h1>
                      <p>Nationality: {{ nationality }}</p>
                      <p>BirthDate: {{ birthdate }}</p>
                      <p>NationalNumber: {{ national_number }}</p>
                  </div>
              </div>
          </div>
      </div>
  </div>
</template>

<script>

  export default {
      name: 'landing-page',
      data(){
          return {
              user: {},
              inserted: false,
              removed: false
          }
      },
      mounted(){
          this.$electron.ipcRenderer.on('beid-read', (event, data) => {
              let json_data = JSON.parse(new TextDecoder("utf-8").decode(data));
              let {action, address, informations, photo} = json_data;
              console.log(action, address, informations, photo, this);

              if(action === 'removed'){
                  this.removed = true;
                  this.inserted = false;
              }else if(action === 'inserted'){
                  this.inserted = true;
                  this.removed = false;
              }else{
                  this.user = {
                      informations,
                      address,
                      photo
                  };
                  this.removed = false;
                  this.inserted = false;
              }
          });
          this.$electron.ipcRenderer.send('beid-read');
      },
      methods: {},
      computed:{
          base64photo(){
              if(!this.user.photo){
                  return ''
              }
              return 'data:image/jpeg;base64,'+this.user.photo
          },
          name(){
              if(!this.user.informations){
                  return ''
              }
              return this.user.informations.last_name + ' ' + this.user.informations.first_name
          },
          nationality(){
              if(!this.user.informations){
                  return ''
              }
              return this.user.informations.nationality
          },
          birthdate(){
              if(!this.user.informations){
                  return ''
              }
              return this.user.informations.birthdate
          },
          national_number(){
              if(!this.user.informations){
                  return ''
              }
              return this.user.informations.national_number
          }
      }
  }
</script>

<style scoped>
    body {
        margin:0px;
    }
    .id-card-wrapper {
        height: 100vh;
        width:100%;
        background-color: #091214;
        display: flex;
    }
    .id-card {
        flex-basis: 100%;
        max-width: 30em;
        border: 1px solid rgb(97, 245, 245);
        margin: auto;
        color: #fff;
        padding: 1em;
        background-color: #0A2129;
        box-shadow: 0px 0px 3px 1px #12a0a0, inset 0px 0px 3px 1px #12a0a0;
    }

    .profile-row {
        display: flex;
    }
    .profile-row .dp {
        flex-basis: 33.3%;
        position: relative;
        margin: 24px;
        align-self: center;
    }
    .profile-row .desc {
        flex-basis: 66.6%;
    }

    .profile-row .dp img {
        max-width: 100%;
        border-radius: 50%;
        display: block;
        box-shadow: 0px 0px 4px 3px #12a0a0;
    }
    .profile-row .desc {
        padding: 1em;
    }

    .profile-row .dp .dp-arc-inner {
        position: absolute;
        width: 100%;
        height: 100%;
        border: 6px solid transparent;
        border-top-color: #0AE0DF;
        border-radius: 50%;
        top: -6px;
        left: -6px;

        animation-duration: 2s;
        animation-name: rotate-clock;
        animation-iteration-count: infinite;
        animation-timing-function: linear;
    }
    @keyframes rotate-clock {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(360deg);
        }
    }
    .profile-row .dp .dp-arc-outer {
        position: absolute;
        width: calc(100% + 20px);
        height: calc(100% + 20px);
        border: 6px solid transparent;
        border-bottom-color: #0AE0DF;
        border-radius: 50%;
        top: -16px;
        left: -16px;

        animation-duration: 2s;
        animation-name: rotate-anticlock;
        animation-iteration-count: infinite;
        animation-timing-function: linear;
    }
    @keyframes rotate-anticlock {
        from {
            transform: rotate(0deg);
        }
        to {
            transform: rotate(-360deg);
        }
    }

    .profile-row .desc {
        font-family: 'Orbitron', sans-serif;
        color: #ecfcfb;
        text-shadow: 0px 0px 4px #12a0a0;
        letter-spacing: 1px;
    }
    .profile-row .desc h1 {
        margin: 0px;
    }
</style>
