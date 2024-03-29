<template>
  <v-data-table :headers="headers" :items="items" class="elevation-1">
    <template v-slot:top>
      <v-toolbar flat>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="500px">
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              color="primary"
              fab
              dark
              class="mb-2"
              v-bind="attrs"
              v-on="on"
            >
              <v-icon dark>mdi-plus</v-icon>
            </v-btn>
          </template>
          <v-card>
            <v-card-title>
              <span class="headline">{{
                $t(`form-data.${formTitle.toLowerCase()}`)
              }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="6"></v-col>
                  <v-col cols="6" class="text-left">
                    <h3>{{ $t("form-data.access-rights") }}</h3>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col cols="12" sm="6" md="6">
                    <v-text-field
                      v-model="editedItem.email"
                      label="Email"
                    ></v-text-field>
                    <v-text-field
                      v-model="editedItem.firstname"
                      :label="$t('table-data.firstname')"
                    ></v-text-field>
                    <v-text-field
                      v-model="editedItem.lastname"
                      :label="$t('table-data.lastname')"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6" md="4">
                    <v-checkbox
                      v-model="editedItem.arrival"
                      :label="$t('table-data.arrival')"
                    ></v-checkbox>
                    <v-checkbox
                      v-model="editedItem.payout"
                      :label="$t('table-data.payout')"
                    ></v-checkbox>
                    <v-checkbox
                      v-model="editedItem.office"
                      :label="$t('table-data.office')"
                    ></v-checkbox>
                  </v-col>
                </v-row>
                <v-row>
                  <div class="text-center" v-if="error">
                    <span class="red--text">{{ error }} </span>
                  </div>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions v-if="!editing && !pending">
              <v-spacer></v-spacer>
              <v-btn color="red darken-1" text @click="close">
                {{ $t("form-data.cancel") }}
              </v-btn>
              <v-btn color="blue darken-1" text @click="invite">
                {{ $t("form-data.invite") }}
              </v-btn>
            </v-card-actions>

            <v-card-actions v-else-if="pending">
              <v-spacer></v-spacer>
              <v-btn color="grey darken-1" text @click="back">
                {{ $t("form-data.back") }}
              </v-btn>
              <v-btn color="red darken-1" text @click="cancelInvite">
                {{ $t("form-data.cancelInvite") }}
              </v-btn>
              <v-btn color="blue darken-1" text @click="reSend">
                {{ $t("form-data.resend") }}
              </v-btn>
            </v-card-actions>

            <v-card-actions v-else-if="editing">
              <v-spacer></v-spacer>
              <v-btn color="grey darken-1" text @click="close">
                {{ $t("form-data.cancel") }}
              </v-btn>
              <v-btn
                color="red darken-1"
                v-if="editedItem.status === `active`"
                text
                @click="deactive"
              >
                {{ $t("form-data.deactive") }}
              </v-btn>
              <v-btn
                color="red darken-1"
                v-if="editedItem.status !== `active`"
                text
                @click="active"
              >
                {{ $t("form-data.active") }}
              </v-btn>
              <v-btn color="blue darken-1" text @click="invite">
                {{ $t("form-data.save") }}
              </v-btn>
            </v-card-actions>

            <v-card-text v-if="error" class="amber darken-1 invite-error">
              {{ $t("messages.invite.error") }}
            </v-card-text>

            <v-card-text v-if="success" class="green darken-1 invite-error">
              {{ $t("messages.invite.success") }}
            </v-card-text>
          </v-card>
        </v-dialog>

        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="headline"
              >Are you sure you want to delete this User?</v-card-title
            >
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete"
                >Cancel</v-btn
              >
              <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                >OK</v-btn
              >
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-toolbar>
    </template>

    <template v-slot:[`header.arrival`]="{ header }">
      {{ $t(`table-data.${header.text.toLowerCase()}`) }}
    </template>
    <template v-slot:[`header.payout`]="{ header }">
      {{ $t(`table-data.${header.text.toLowerCase()}`) }}
    </template>
    <template v-slot:[`header.office`]="{ header }">
      {{ $t(`table-data.${header.text.toLowerCase()}`) }}
    </template>
    <template v-slot:[`header.actions`]="{ header }">
      {{ $t(`table-data.${header.text.toLowerCase()}`) }}
    </template>

    <template v-slot:[`item.arrival`]="{ item }">
      <v-simple-checkbox v-model="item.arrival" disabled></v-simple-checkbox>
    </template>
    <template v-slot:[`item.payout`]="{ item }">
      <v-simple-checkbox v-model="item.payout" disabled></v-simple-checkbox>
    </template>
    <template v-slot:[`item.office`]="{ item }">
      <v-simple-checkbox v-model="item.office" disabled></v-simple-checkbox>
    </template>
    <template v-slot:[`item.status`]="{ item }">
      {{ $t(`table-data.${item.status.toLowerCase()}`) }}
    </template>
    <template v-slot:[`item.actions`]="{ item }">
      <v-icon small class="mr-2" @click="editItem(item)">
        mdi-pencil
      </v-icon>
      <v-icon small @click="deleteItem(item)">
        mdi-delete
      </v-icon>
    </template>

    <template v-slot:no-data>
      <v-btn color="primary" @click="initialize">
        Reset
      </v-btn>
    </template>
  </v-data-table>
</template>

<script>
import {
  inviteUser,
  deleteUser,
  updateUser,
  cancelInviteUser,
  getUsers
} from '../../api'
export default {
  name: 'users',
  data: () => ({
    dialog: false,
    dialogDelete: false,
    pending: false,
    editing: false,
    error: null,
    success: false,
    headers: [
      { text: 'Name', value: 'name' },
      { text: 'Email', value: 'email' },
      { text: 'Arrival', value: 'arrival' },
      { text: 'Payout', value: 'payout' },
      { text: 'Office', value: 'office' },
      { text: 'Status', value: 'status' },
      { text: 'Actions', value: 'actions', sortable: false }
    ],
    items: [],
    editedIndex: -1,
    editedItem: {
      id: '',
      firstname: '',
      lastname: '',
      email: '',
      arrival: false,
      payout: false,
      office: false
    },
    defaultItem: {
      id: '',
      firstname: '',
      lastname: '',
      email: '',
      arrival: false,
      payout: false,
      office: false
    }
  }),

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'Invite User' : 'Edit User'
    }
  },

  watch: {
    dialog (val) {
      val || this.close()
    },
    dialogDelete (val) {
      val || this.closeDelete()
    }
  },

  created () {
    this.initialize()
  },

  methods: {
    initialize () {
      const csrftoken = document
        .querySelector('input[name="csrfmiddlewaretoken"]')
        .getAttribute('value')
      // eslint-disable-next-line no-undef
      getUsers(csrftoken)
        .then((res) => res.json())
        .then(({ result }) => {
          // eslint-disable-next-line no-undef
          this.items = result.map((item) => ({
            name: item.firstname + ' ' + item.lastname,
            ...item
          }))
        })
    },

    editItem (item) {
      this.editedIndex = this.items.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
      this.editing = true
    },

    deleteItem (item) {
      this.editedIndex = this.items.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },

    async deleteItemConfirm () {
      this.items.splice(this.editedIndex, 1)
      // eslint-disable-next-line no-undef
      await deleteUser(this.editedItem.id, csrftoken)
      this.closeDelete()
    },

    back () {
      this.pending = false
    },

    close () {
      this.dialog = false
      this.editing = false
      this.pending = false
      this.error = null
      this.success = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    closeDelete () {
      this.dialogDelete = false
      this.editedItem = Object.assign({}, this.defaultItem)
      this.editedIndex = -1
    },

    async invite () {
      if (this.editedIndex > -1) {
        delete this.editedItem.name
        // eslint-disable-next-line no-undef
        updateUser(this.editedItem, csrftoken).then(() => {
          Object.assign(this.items[this.editedIndex], {
            ...this.editedItem,
            name: this.editedItem.firstname + ' ' + this.editedItem.lastname
          })
          this.close()
        })
      } else {
        this.validation()
        if (!this.error) {
          this.pending = true
          delete this.editedItem.name
          delete this.editedItem.id
          // eslint-disable-next-line no-undef
          inviteUser(this.editedItem, csrftoken)
            .then((res) => res.json())
            .then((res) => {
              if (res.result === 'success') {
                this.success = true
              } else {
                this.error = 'Something went wrong.'
              }
            })
        }
      }
    },

    deactive () {
      if (this.editedIndex > -1) {
        this.editedItem.status = 'Deactivated'
        delete this.editedItem.name
        // eslint-disable-next-line no-undef
        updateUser(this.editedItem, csrftoken).then(() => {
          this.initialize()
          this.close()
        })
      }
    },

    active () {
      if (this.editedIndex > -1) {
        this.editedItem.status = 'active'
        delete this.editedItem.name
        // eslint-disable-next-line no-undef
        updateUser(this.editedItem, csrftoken).then(() => {
          this.initialize()
          this.close()
        })
      }
    },

    reSend () {
      // eslint-disable-next-line no-undef
      inviteUser(this.editedItem, csrftoken)
    },

    cancelInvite () {
      const data = {
        email: this.editedItem.email
      }
      // eslint-disable-next-line no-undef
      cancelInviteUser(data, csrftoken)
      this.close()
    },
    validation () {
      if (!this.editedItem.email) {
        this.error = 'Please enter email address.'
      } else if (!this.editedItem.firstname) {
        this.error = 'Please enter First Name.'
      } else if (!this.editedItem.lastname) {
        this.error = 'Please enter Last Name.'
      } else {
        this.error = null
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.v-data-table {
  margin-left: 260px;
}
.invite-error {
  color: white !important;
  padding-top: 10px !important;
}
</style>
