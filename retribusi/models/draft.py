from odoo import fields, models, api


class kmk_draft(models.Model):
    _name = 'kmk.draft'
    _description = 'Description'

    id = fields.Char(string='Id', required=False)
    name = fields.Char(string="Nama Pemilik/Perusahaan")
    lokasi = fields.Text(string="Lokasi",
                         required=False)
    tahun = fields.Integer(string='Tahun Bangunan',
                           required=False)
    status = fields.Selection(string='Status',
                              selection=[('draft', 'Draft'),
                                         ('data_bangunan', 'Parameter'),
                                         ('prasarana', 'Prasarana'),
                                         ('done', 'Done'), ],
                              required=False,
                              default='draft')
    #configurating state
    def action_confirm(self):
        for rec in self:
            rec.status = 'data_bangunan'

    def action_ok(self):
        for rec in self:
            rec.status = 'prasarana'

    #record state == data bangunan
    fungsi = fields.Selection(string='Fungsi Bangunan',
                              selection=[('fungsi_1', 'Hunian (< 100m² dan <2 Lantai)'),
                                         ('fungsi_2', 'Hunian (> 100m² dan >2 Lantai)'),
                                         ('fungsi_3', 'Keagamaan'),
                                         ('fungsi_4', 'Usaha'),
                                         ('fungsi_5', 'Usaha UMKM'),
                                         ('fungsi_6', 'Sosial & Budaya'),
                                         ('fungsi_7', 'Khusus'),
                                         ('fungsi_8', 'Ganda Campuran (≤ 500m² dan ≤ 2 Lantai'),
                                         ('fungsi_9', 'Ganda Campuran (≥ 500m² dan ≥ 2 Lantai')],
                              required=False, )

    index_fungsi = fields.Float(string='Indeks Fungsi(If)',
                           required=False,
                           nolabel=True)

    @api.onchange('fungsi')
    def _onchange_fungsi(self):
        if self.fungsi == 'fungsi_1':
            self.index_fungsi = 0.15
        elif self.fungsi == 'fungsi_2':
            self.index_fungsi = 0.17
        elif self.fungsi == 'fungsi_3':
            self.index_fungsi = 0
        elif self.fungsi == 'fungsi_4':
            self.index_fungsi = 0.7
        elif self.fungsi == 'fungsi_5':
            self.index_fungsi = 0.5
        elif self.fungsi == 'fungsi_6':
            self.index_fungsi = 0.3
        elif self.fungsi == 'fungsi_7':
            self.index_fungsi = 1
        elif self.fungsi == 'fungsi_8':
            self.index_fungsi = 0.6
        elif self.fungsi == 'fungsi_9':
            self.index_fungsi = 0.8
        else :
            self.index_fungsi = 0

    faktor_kepemilikan = fields.Selection(string='Faktor Kepemilikan',
                                         selection=[('negara', 'Negara'),
                                                    ('perorangan', 'Perorangan/Badan Usaha'), ],
                                         required=False, )

    indeks_kepemilikan = fields.Integer(
        string='Indeks Kepemilikan (Fm)',
        required=False)

    @api.onchange('faktor_kepemilikan')
    def _onchange_faktor_kepemilikan(self):
        if self.faktor_kepemilikan == 'negara':
            self.indeks_kepemilikan = 0
        elif self.faktor_kepemilikan == 'perorangan':
            self.indeks_kepemilikan = 1
        else:
            self.indeks_kepemilikan = 0

    permanensi = fields.Selection(string='Permanensi',
                                  selection=[('permanen', 'Permanen'),
                                             ('non_permanen', 'Non Permanen'), ],
                                  required=False, )
    indeks_permanensi = fields.Float(
        string='Indeks_permanensi',
        required=False)
    bobot_permanensi = fields.Float(
        string='bobot_permanensi',
        required=False,
        default=0.2)
    sum_permanensi = fields.Float(
        string='Sum_permanensi',
        required=False,
        compute='_compute_sum_permanensi')


    @api.onchange('permanensi')
    def _onchange_permanensi(self):
        if self.permanensi == 'permanen':
            self.indeks_permanensi = 2
        elif self.permanensi == 'non_permanen':
            self.indeks_permanensi = 1
        else:
            self.indeks_permanensi = 0

    @api.depends('indeks_permanensi', 'bobot_permanensi')
    def _compute_sum_permanensi(self):
        for record in self:
            record.sum_permanensi = record.indeks_permanensi * record.bobot_permanensi

    kompleksitas = fields.Selection(string='Kompleksitas',
                                    selection=[('sederhana', 'Sederhana'),
                                               ('tidak_sederhana', 'Tidak Sederhana'), ],
                                    required=False, )

    bobot_kompleksitas = fields.Float(string='Bobot Kompleksitas',
                                      required=False,
                                      default=0.3)
    sum_kompleksitas = fields.Float(string='Nilai Kompleksitas',
                                    required=False,
                                    compute='_compute_sum_kompleksitas')

    indeks_kompleksitas = fields.Float(string='Indeks Kompleksitas',
                                       required=False)

    @api.onchange('kompleksitas')
    def _onchange_kompleksitas(self):
        if self.kompleksitas == 'sederhana':
            self.indeks_kompleksitas = 1
        elif self.kompleksitas == 'tidak_sederhana':
            self.indeks_kompleksitas = 2
        else:
            self.indeks_kompleksitas = 0

    @api.depends('indeks_kompleksitas', 'bobot_kompleksitas')
    def _compute_sum_kompleksitas(self):
        for record in self:
            record.sum_kompleksitas = record.indeks_kompleksitas * record.bobot_kompleksitas

    # ketinggian = fields.Selection(string='Ketinggian',
    #                               selection=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'),
    #                                          ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'),
    #                                          ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'),
    #                                          ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'),
    #                                          ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'), ('50', '50'),
    #                                          ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'), ('56', '56'), ('57', '57'), ('58', '58'), ('59', '59'), ('60', '60'), ],
    #                               required=False, )
    ketinggian = fields.Integer(
        string='Jumlah Lantai',
        required=False)

    tinggi_bangunan = fields.Float(
        string='Tinggi Bangunan',
        required=False)
    lantai_basement= fields.Integer(
        string='Jumlah lantai Basement',
        required=False)
    luas_basement = fields.Float(
        string='Luas Basement',
        required=False)
    bobot_ketinggian = fields.Float(string='Bobot Ketinggian',
                                    required=False,
                                    default=0.5)
    sum_ketinggian = fields.Float(string='Nilai Ketinggian',
                                  required=False,
                                  compute='_compute_sum_ketinggian',
                                  digits=(12, 3))

    indeks_ketinggian = fields.Float(string='Indeks Ketinggian',
                                     required=False,
                                     digits=(12, 3))

    @api.onchange('ketinggian')
    def _onchange_ketinggian(self):
        if self.ketinggian == 1:
            self.indeks_ketinggian = 1
        elif self.ketinggian == 2:
            self.indeks_ketinggian = 1.090
        elif self.ketinggian == 3:
            self.indeks_ketinggian = 1.120
        elif self.ketinggian == 4:
            self.indeks_ketinggian = 1.135
        elif self.ketinggian == 5:
            self.indeks_ketinggian = 1.162
        elif self.ketinggian == 6:
            self.indeks_ketinggian = 1.197
        elif self.ketinggian == 7:
            self.indeks_ketinggian = 1.236
        elif self.ketinggian == 8:
            self.indeks_ketinggian = 1.265
        elif self.ketinggian == 9:
            self.indeks_ketinggian = 1.299
        elif self.ketinggian == 10:
            self.indeks_ketinggian = 1.333
        elif self.ketinggian == 11:
            self.indeks_ketinggian = 1.364
        elif self.ketinggian == 12:
            self.indeks_ketinggian = 1.393
        elif self.ketinggian == 13:
            self.indeks_ketinggian = 1.420
        elif self.ketinggian == 14:
            self.indeks_ketinggian = 1.445
        elif self.ketinggian == 15:
            self.indeks_ketinggian = 1.468
        elif self.ketinggian == 16:
            self.indeks_ketinggian = 1.489
        elif self.ketinggian == 17:
            self.indeks_ketinggian = 1.508
        elif self.ketinggian == 18:
            self.indeks_ketinggian = 1.525
        elif self.ketinggian == 19:
            self.indeks_ketinggian = 1.541
        elif self.ketinggian == 20:
            self.indeks_ketinggian = 1.556
        elif self.ketinggian == 21:
            self.indeks_ketinggian = 1.570
        elif self.ketinggian == 22:
            self.indeks_ketinggian = 1.584
        elif self.ketinggian == 23:
            self.indeks_ketinggian = 1.597
        elif self.ketinggian == 24:
            self.indeks_ketinggian = 1.610
        elif self.ketinggian == 25:
            self.indeks_ketinggian = 1.622
        elif self.ketinggian == 26:
            self.indeks_ketinggian = 1.634
        elif self.ketinggian == 27:
            self.indeks_ketinggian = 1.645
        elif self.ketinggian == 28:
            self.indeks_ketinggian = 1.656
        elif self.ketinggian == 29:
            self.indeks_ketinggian = 1.666
        elif self.ketinggian == 30:
            self.indeks_ketinggian = 1.676
        elif self.ketinggian == 31:
            self.indeks_ketinggian = 1.686
        elif self.ketinggian == 32:
            self.indeks_ketinggian = 1.695
        elif self.ketinggian == 33:
            self.indeks_ketinggian = 1.704
        elif self.ketinggian == 34:
            self.indeks_ketinggian = 1.713
        elif self.ketinggian == 35:
            self.indeks_ketinggian = 1.722
        elif self.ketinggian == 36:
            self.indeks_ketinggian = 1.730
        elif self.ketinggian == 37:
            self.indeks_ketinggian = 1.738
        elif self.ketinggian == 38:
            self.indeks_ketinggian = 1.746
        elif self.ketinggian == 39:
            self.indeks_ketinggian = 1.754
        elif self.ketinggian == 40:
            self.indeks_ketinggian = 1.761
        elif self.ketinggian == 41:
            self.indeks_ketinggian = 1.768
        elif self.ketinggian == 42:
            self.indeks_ketinggian = 1.775
        elif self.ketinggian == 43:
            self.indeks_ketinggian = 1.782
        elif self.ketinggian == 44:
            self.indeks_ketinggian = 1.789
        elif self.ketinggian == 45:
            self.indeks_ketinggian = 1.795
        elif self.ketinggian == 46:
            self.indeks_ketinggian = 1.801
        elif self.ketinggian == 47:
            self.indeks_ketinggian = 1.807
        elif self.ketinggian == 48:
            self.indeks_ketinggian = 1.813
        elif self.ketinggian == 49:
            self.indeks_ketinggian = 1.818
        elif self.ketinggian == 50:
            self.indeks_ketinggian = 1.823
        elif self.ketinggian == 51:
            self.indeks_ketinggian = 1.828
        elif self.ketinggian == 52:
            self.indeks_ketinggian = 1.833
        elif self.ketinggian == 53:
            self.indeks_ketinggian = 1.837
        elif self.ketinggian == 54:
            self.indeks_ketinggian = 1.841
        elif self.ketinggian == 55:
            self.indeks_ketinggian = 1.845
        elif self.ketinggian == 56:
            self.indeks_ketinggian = 1.849
        elif self.ketinggian == 57:
            self.indeks_ketinggian = 1.853
        elif self.ketinggian == 58:
            self.indeks_ketinggian = 1.856
        elif self.ketinggian == 59:
            self.indeks_ketinggian = 1.859
        elif self.ketinggian == 60:
            self.indeks_ketinggian = 1.862

    @api.depends('indeks_ketinggian', 'bobot_ketinggian')
    def _compute_sum_ketinggian(self):
        for record in self:
            record.sum_ketinggian = record.indeks_ketinggian * record.bobot_ketinggian

    sum_index = fields.Float(
        string='Σ(Bp x Ip)',
        required=False,
        compute='_compute_sum_index',
        digits=(12,3))

    @api.depends('sum_kompleksitas', 'sum_permanensi','sum_ketinggian' )
    def _compute_sum_index(self):
        for record in self:
            sum_index = record.sum_kompleksitas + record.sum_permanensi + record.sum_ketinggian
            record.sum_index = sum_index

    indeks_terintegrasi = fields.Float(
        string='Indeks Terintegrasi',
        compute='_compute_indeks_terintegrasi',
        required=False)

    @api.depends('index_fungsi', 'indeks_kepemilikan', 'sum_index')
    def _compute_indeks_terintegrasi(self):
        for record in self:
            indeks_terintegrasi = record.index_fungsi * record.indeks_kepemilikan * record.sum_index
            record.indeks_terintegrasi = indeks_terintegrasi

    luas_bangunan = fields.Float(string='Luas Bangunan (LLt)',
                                 required=False)
    
    shst = fields.Integer(string='SATUAN HARGA STANDAR TERTINGGI (SHST)',
                          required=False,
                          default=6750000)
    
    indeks_lokalitas = fields.Float(string='Indeks Lokalitas (Ilo)',
                                    required=False,
                                    default=0.5)

    jenis_pembangunan = fields.Selection(string='Jenis Pembangunan',
                                       selection=[('pembangunan_1', 'Pembangunan Gedung Baru'),
                                                  ('pembangunan_2', 'Rehabilitasi/Renovasi Bangunan - Sedang'),
                                                  ('pembangunan_3', 'Rehabilitasi/Renovasi Bangunan - Berat'),
                                                  ('pembangunan_4', 'Rusak Berat - Pelestarian Pratama'),
                                                  ('pembangunan_5', 'Rusak Sedang - Pelestarian Madya'),
                                                  ('pembangunan_6', 'Pelestarian Utama'),

                                                  ],
                                       required=False, )
    indeks_terbangun = fields.Float(string='Indeks BG Terbangun (Ibg)',
                                    required=False,
                                    digits=(12,3))



    @api.onchange('jenis_pembangunan')
    def _onchange_jenis_pembangunan(self):
        if self.jenis_pembangunan == 'pembangunan_1':
            self.indeks_terbangun = 1
        elif self.jenis_pembangunan == 'pembangunan_2':
            self.indeks_terbangun = 0.225
        elif self.jenis_pembangunan == 'pembangunan_3':
            self.indeks_terbangun = 0.325
        elif self.jenis_pembangunan == 'pembangunan_4':
            self.indeks_terbangun = 0.325
        elif self.jenis_pembangunan == 'pembangunan_5':
            self.indeks_terbangun = 0.225
        elif self.jenis_pembangunan == 'pembangunan_6':
            self.indeks_terbangun = 0.150
        else:
            self.indeks_terbangun = 0
            
    nilai_retribusi = fields.Float(
        string='Nilai Retribusi',
        compute='_compute_nilai_retribusi',
        required=False)

    @api.depends('luas_bangunan', 'indeks_lokalitas', 'shst', 'indeks_terintegrasi', 'indeks_terbangun')
    def _compute_nilai_retribusi(self):
        for record in self:
            nilai_retribusi = record.luas_bangunan * (record.indeks_lokalitas * record.shst) * record.indeks_terintegrasi * record.indeks_terbangun
            record.nilai_retribusi = nilai_retribusi

    #PRASARANA


    prasarana_id = fields.Many2one(
        comodel_name='kmk.prasarana',
        string='Prasarana ID',
        required=False)

    konstruksi_1 = fields.Boolean(
        string='Konstruksi pembatas/penahan/pengaman',
        required=False)

    bangunan_1 = fields.Boolean(string='Pagar',
                                required=False)

    class kmk_prasarana(models.Model):
        _name = 'kmk.prasarana'
        _description = 'kmk_prasarana'
        
        name = fields.Char(
            string='Name', 
            required=False)
        
        prasarana = fields.Selection(
            string='Prasarana',
            selection=[('konstruksi_1', 'Konstruksi pembatas/penahan/pengaman'),
                       ('konstruksi_2', 'Konstruksi penanda masuk lokasi'),
                       ('konstruksi_3', 'Konstruksi perkerasan'),
                       ('konstruksi_4', 'Konstruksi perkerasan aspal, beton'),
                       ('konstruksi_5', 'Konstruksi perkerasan grassblock'),
                       ('konstruksi_6', 'Konstruksi penghubung'),
                       ('konstruksi_7', 'Konstruksi penghubung (jembatan antar gedung)'),
                       ('konstruksi_8', 'Konstruksi penghubung (jembatan penyebrangan orang/barang)'),
                       ('konstruksi_9', 'Konstruksi penghubung (jembatan bawah tanah/underpass)'),
                       ('konstruksi_10', 'Konstruksi kolam/reservoir bawah tanah'),
                       ('konstruksi_11', 'Konstruksi septic tank, sumur resapan'),
                       ('konstruksi_12', 'Konstruksi menara'),
                       ('konstruksi_13', 'KKonstruksi menara air'),
                       ('konstruksi_14', 'Konstruksi monumen'),
                       ('konstruksi_15', 'Konstruksi instalasi/gardu listrik'),
                       ('konstruksi_16', 'Konstruksi reklame/papan nama'),
                       ('konstruksi_17', 'Konstruksi pondasi mesin'),
                       ('konstruksi_18', 'Konstruksi Menara televisi'),
                       ('konstruksi_19', 'Konstruksi Antena Radio - Standing tower dengan konstruksi 3-4 kaki'),
                       ('konstruksi_20', 'Konstruksi Antena Radio - Sistem guy wire/bentang kawat'),
                       ('konstruksi_21', 'Konstruksi antenna (tower telekomunikasi) - Menara Bersama'),
                       ('konstruksi_22', 'Konstruksi antenna (tower telekomunikasi) - Menara Mandiri'),
                       ('konstruksi_23', 'Tangki tanam bahan bakar'),
                       ('konstruksi_24', 'Pekerjaan drainase (dalam persil)'),
                       ('konstruksi_25', 'Konstruksi penyimpanan/Silo'),
                       ('konstruksi_26', 'Gapura')
                       ],
            required=False, )

        satuan = fields.Selection(string='Satuan',
                                  selection=[('unit_1', 'm'),
                                             ('unit_2', 'm²'),
                                             ('unit_3', 'Per 5 m²'),
                                             ('unit_4', 'Unit'),
                                             ('unit_5', 'Unit (luas maksimum 10 m²'),
                                             ('unit_6',
                                              'Unit dan penambahannya (luas konstruksi reklame maksimum 30 m²)'),
                                             ('unit_7', 'Unit mesin'),
                                             ('unit_8',
                                              'Unit (tinggi maksimal 100 m, selebihnya dihitung kelipatannya)'),
                                             ('unit_9', 'm³')],
                                  required=False, )





