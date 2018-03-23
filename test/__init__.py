import vcr as _vcr
vcr = _vcr.VCR(record_mode='none')

cassettes = {
    'ers':  'test/resources/ers-cassette.yaml',
    'm2m':  'test/resources/m2m-cassette.yaml',
    'tram': 'test/resources/tram-cassette.yaml',
}

import hypothesis
