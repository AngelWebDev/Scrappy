<template>
  <v-data-table
    :headers="headers"
    :items="items"
    :search="search"
    class="elevation-1"
  >
    <template v-slot:top>
      <v-toolbar flat>
        <v-text-field
          v-model="search"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
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
                  <v-col cols="7" sm="7">
                    <v-row>
                      <v-col cols="4">
                        <v-select
                          outlined
                          :items="solutations"
                          :label="$t('table-data.solutation')"
                          v-model="editedItem.title"
                        ></v-select>
                      </v-col>
                      <v-col cols="8">
                        <v-text-field
                          outlined
                          v-model="editedItem.email"
                          label="Email"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col cols="6">
                        <v-text-field
                          outlined
                          v-model="editedItem.firstname"
                          :label="$t('table-data.firstname')"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="6">
                        <v-text-field
                          outlined
                          v-model="editedItem.lastname"
                          :label="$t('table-data.lastname')"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <v-text-field
                      outlined
                      v-model="editedItem.street"
                      :label="$t('table-data.address')"
                    ></v-text-field>
                    <v-row>
                      <v-col cols="6">
                        <v-text-field
                          outlined
                          v-model="editedItem.zip"
                          :label="$t('table-data.zip')"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="6">
                        <v-text-field
                          outlined
                          v-model="editedItem.city"
                          :label="$t('table-data.city')"
                        ></v-text-field>
                      </v-col>
                    </v-row>

                    <v-text-field
                      outlined
                      v-model="editedItem.phone1"
                      :label="$t('table-data.phone')"
                    ></v-text-field>
                    <v-textarea
                      outlined
                      v-model="editedItem.comments"
                      :label="$t('table-data.comments')"
                    ></v-textarea>
                  </v-col>

                  <v-col cols="5">
                    <v-switch
                      outlined
                      class="mb-11"
                      v-model="is_company"
                      :value="is_company"
                      inset
                      :label="$t('table-data.is_company')"
                    />
                    <v-text-field
                      outlined
                      v-show="is_company"
                      v-model="editedItem.company.name"
                      :label="$t('table-data.company_name')"
                    />
                    <v-text-field
                      outlined
                      v-show="is_company"
                      v-model="editedItem.company.vat_id"
                      :label="$t('table-data.vat_id')"
                    />
                    <v-text-field
                      outlined
                      v-show="is_company"
                      v-model="editedItem.company.tax_id"
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
                    <v-btn color="blue darken-1" text @click="save">
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

    <template v-slot:[`header.firstname`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.lastname`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.address`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.city`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.comments`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.vat_id`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.status`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>
    <template v-slot:[`header.actions`]="{ header }">
      {{ $t(`table-data.${header.value}`) }}
    </template>

    <template v-slot:[`item.status`]="{ item }">
      {{ $t(`table-data.${item.status ? "active" : "pending"}`) }}
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
import { createCustomer, updateCustomer, deactiveCustomer } from "../../api";
export default {
  name: "customers",
  data: () => ({
    dialog: false,
    dialogDelete: false,
    pending: false,
    editing: false,
    search: "",
    is_company: false,
    solutations: ["Mr", "Mrs", "Dr", "Prof"],
    headers: [
      { text: "No", value: "no" },
      { text: "Last Name", value: "lastname" },
      { text: "First Name", value: "firstname" },
      { text: "Address", value: "street" },
      { text: "City", value: "city" },
      { text: "Comments", value: "comments" },
      { text: "Vat_id", value: "company.vat_id" },
      { text: "Status", value: "status" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    items: [],
    editedIndex: -1,
    editedItem: {
      title: "",
      firstname: "",
      lastname: "",
      street: "",
      city: "",
      comments: "",
      status: true,
      phone1: "",
      zip: "",
      email: "",
      company: {
        id: "",
        name: "",
        tax_id: "",
        vat_id: "",
      },
    },
    defaultItem: {
      title: "",
      firstname: "",
      lastname: "",
      street: "",
      city: "",
      phone1: "",
      comments: "",
      status: true,
      zip: "",
      email: "",
      company: {
        id: "",
        name: "",
        tax_id: "",
        vat_id: "",
      },
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
      this.items = customers.map((item, index) => ({ ...item, no: index + 1 }));
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

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.items[this.editedIndex], this.editedItem);
        updateCustomer(this.editedItem);
        this.editing = true;
      } else {
        if (this.editedItem.email) {
          if (this.editedItem.company.id === "") {
            delete this.editedItem.company.id;
          }
          createCustomer(this.editedItem);
          this.items.push({ ...this.editedItem, no: this.items.length + 1 });
        }
      }
      this.close();
    },

    deactive() {
      deactiveCustomer(this.editedItem.id);
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.v-data-table {
  margin-left: 260px;
}
</style>
