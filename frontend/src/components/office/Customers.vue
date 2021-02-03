<template>
  <v-data-table :headers="headers" :items="items" class="elevation-1">
    <template v-slot:top>
      <v-toolbar flat>
        <v-spacer></v-spacer>
        <v-dialog v-model="dialog" max-width="900px">
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
              <span class="headline">{{ $t(`form-data.${formTitle}`) }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="6" sm="6">
                    <v-select
                      :items="solutations"
                      :label="$t('table-data.solutation')"
                      v-model="editedItem.title"
                    ></v-select>
                    <v-text-field
                      v-model="editedItem.firstname"
                      :label="$t('table-data.firstname')"
                    ></v-text-field>
                    <v-text-field
                      v-model="editedItem.lastname"
                      :label="$t('table-data.lastname')"
                    ></v-text-field>
                    <v-text-field
                      v-model="editedItem.address"
                      :label="$t('table-data.address')"
                    ></v-text-field>
                    <v-text-field
                      v-model="editedItem.zip"
                      :label="$t('table-data.zip')"
                    ></v-text-field>
                    <v-text-field
                      v-model="editedItem.city"
                      :label="$t('table-data.city')"
                    ></v-text-field>
                    <v-text-field
                      v-model="editedItem.email"
                      label="Email"
                    ></v-text-field>
                    <v-text-field
                      v-model="editedItem.phone"
                      :label="$t('table-data.phone')"
                    ></v-text-field>
                    <v-text-field
                      v-model="editedItem.comments"
                      :label="$t('table-data.comments')"
                    ></v-text-field>
                  </v-col>

                  <v-col cols="6">
                    <v-switch
                      v-model="editedItem.is_company"
                      inset
                      :label="$t('table-data.is_company')"
                    />
                    <v-text-field
                      v-model="editedItem.company_name"
                      :label="$t('table-data.company_name')"
                    />
                    <v-text-field
                      v-model="editedItem.vat_id"
                      :label="$t('table-data.vat_id')"
                    />
                    <v-text-field
                      v-model="editedItem.tax_id"
                      :label="$t('table-data.tax_id')"
                    />
                    <div class="text-right mt-16 pt-16">
                      <v-btn color="warning" dark>
                        {{ $t("table-data.verify") }}
                      </v-btn>
                    </div>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-container>
                <v-row>
                  <v-col cols="9">
                    <v-btn color="grey darken-1" text @click="close">
                      {{ $t("form-data.cancel") }}
                    </v-btn>
                    <v-btn color="red darken-1" text @click="deactive">
                      {{ $t("form-data.deactive") }}
                    </v-btn>
                  </v-col>

                  <v-col cols="3">
                    <v-btn color="blue darken-1" text @click="invite">
                      {{ $t("form-data.save") }}
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-actions>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="headline"
              >Are you sure you want to delete this item?</v-card-title
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
export default {
  name: "customers",
  data: () => ({
    dialog: false,
    dialogDelete: false,
    pending: false,
    editing: false,
    solutations: ["Mr", "Mrs", "Dr", "Prof"],
    headers: [
      { text: "No", value: "no" },
      { text: "Last Name", value: "lastname" },
      { text: "First Name", value: "firstname" },
      { text: "Address", value: "address" },
      { text: "City", value: "city" },
      { text: "Comments", value: "comments" },
      { text: "Vat_id", value: "vat_id" },
      { text: "Status", value: "status" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    items: [],
    editedIndex: -1,
    editedItem: {
      title: "",
      firstname: "",
      lastname: "",
    },
    defaultItem: {
      name: "",
      email: "",
      arrival: false,
      payout: false,
      office: false,
      status: "",
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "create-customer" : "edit-customer";
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    this.initialize();
  },

  methods: {
    initialize() {
      // eslint-disable-next-line no-undef
      this.items = users.map((item, index) => ({ ...item, no: index + 1 }));
    },

    editItem(item) {
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialog = true;
      this.editing = true;
    },

    deleteItem(item) {
      this.editedIndex = this.items.indexOf(item);
      this.editedItem = Object.assign({}, item);
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.items.splice(this.editedIndex, 1);
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.editing = false;
      this.pending = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    invite() {
      if (this.editedIndex > -1) {
        Object.assign(this.items[this.editedIndex], this.editedItem);
        this.editing = true;
      } else {
        if (this.editedItem.email && this.editedItem.name) {
          this.editedItem.status = "invitation pending";
          this.pending = true;
        }
      }
    },

    deactive() {},
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.v-data-table {
  margin-left: 260px;
}
</style>
