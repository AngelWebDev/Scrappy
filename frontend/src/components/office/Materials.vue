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
              <span class="headline">{{ $t(`form-data.${formTitle}`) }}</span>
            </v-card-title>

            <v-card-text>
              <v-container>
                <v-row>
                  <v-col>
                    <v-text-field
                      outlined
                      v-model="editedItem.name"
                      :label="$t('table-data.name')"
                    />
                    <v-text-field
                      outlined
                      v-model="editedItem.price_per_kg"
                      :label="$t('table-data.price_per_kg')"
                    />
                  </v-col>
                </v-row>
                <div class="text-center" v-if="error">
                  <span class="red--text">{{ error }} </span>
                </div>
              </v-container>
            </v-card-text>

            <v-card-actions>
              <v-container>
                <v-row>
                  <v-col cols="6">
                    <v-btn color="grey darken-1" text @click="close">
                      {{ $t("form-data.cancel") }}
                    </v-btn>
                  </v-col>

                  <v-col cols="6">
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
              >Are you sure you want to delete this Material?</v-card-title
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
  createMaterial,
  getMaterial,
  updateMaterial,
  deleteMaterial,
  getMaterials,
} from "../../api";
export default {
  name: "materials",
  data: () => ({
    dialog: false,
    dialogID: false,
    dialogDelete: false,
    token: "",
    error: "",

    headers: [
      { text: "No", value: "no" },
      { text: "Name", value: "name" },
      { text: "Price", value: "price_per_kg" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    items: [],
    editedIndex: -1,
    editedItem: {
      id: "",
      name: "",
      price_per_kg: 0.0,
    },
    defaultItem: {
      id: "",
      name: "",
      price_per_kg: 0.0,
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "create-material" : "edit-material";
    },
  },

  mounted() {
    this.token = document
      .querySelector('input[name="csrfmiddlewaretoken"]')
      .getAttribute("value");
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
      getMaterials(this.token)
        .then((res) => res.json())
        .then(({ result }) => {
          this.items = result.map((item, index) => ({
            ...item,
            no: index + 1,
          }));
        });
    },

    editItem(item) {
      getMaterial(item.id, this.token).then((res) => {
        console.log("angel log", res);
        if (res) {
          this.editedIndex = this.items.indexOf(item);
          this.editedItem = Object.assign({}, res.result);
          this.dialog = true;
          this.editing = true;
        }
      });
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
      this.error = "";
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      deleteMaterial(this.editedItem.id, this.token);
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem);
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.items[this.editedIndex], this.editedItem);

        updateMaterial(this.editedItem, this.token).then((res) => {
          if (res.ok) {
            this.editing = true;
            this.close();
          } else {
            this.error = res.statusText;
          }
        });
      } else {
        if (this.editedItem.name) {
          delete this.editedItem.id;
          createMaterial(this.editedItem, this.token)
            .then((res) => res.json())
            .then((res) => {
              if (res.result) {
                this.items.push({
                  ...res.result,
                  no: this.items.length + 1,
                });
                this.close();
              } else {
                this.error = "Something went wrong.";
              }
            });
        }
      }
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
