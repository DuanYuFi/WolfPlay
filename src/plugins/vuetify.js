import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import 'vuetify/dist/vuetify.min.css'

Vue.use(Vuetify)

const vuetify = new Vuetify({
    theme: {
      themes: {
        dark: {
          primary: '#333333',
          anchor: '#333333',
        },
      },
    },
  })

export default vuetify